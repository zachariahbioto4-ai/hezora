import os
import mimetypes
from django.http import (
    FileResponse, Http404, HttpResponseForbidden
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404, render, redirect
)
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import (
    DownloadToken, PurchasedBook, DownloadLog
)
from orders.models import Order


@login_required
def delivery_page(request, order_id):
    """Post-purchase page — lists all download links."""
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
        payment_status='completed'
    )
    tokens = DownloadToken.objects.filter(
        order=order, user=request.user
    ).select_related('book_file__book')

    return render(request,
        'delivery/delivery_page.html',
        {'order': order, 'tokens': tokens}
    )


@login_required
def download_file(request, token_uuid):
    """Secure download via email token.
    Checks: ownership, expiry, download count."""
    token = get_object_or_404(
        DownloadToken, token=token_uuid
    )

    # ── Security check: ownership ─────────────────
    if token.user != request.user:
        DownloadLog.objects.create(
            token=token, user=request.user,
            ip_address=_get_ip(request),
            user_agent=request.META.get(
                'HTTP_USER_AGENT', ''),
            success=False
        )
        return HttpResponseForbidden(
            "This link does not belong to your account."
        )

    # ── Security check: validity ──────────────────
    if not token.is_valid:
        msg = (
            "This download link has expired."
            if timezone.now() >= token.expires_at
            else "Download limit reached for this link."
        )
        return render(request,
            'delivery/link_expired.html',
            {'message': msg, 'token': token},
            status=410
        )

    # ── Serve the file ────────────────────────────
    book_file = token.book_file
    file_path = book_file.file.path

    if not os.path.exists(file_path):
        raise Http404("File not found on server.")

    content_type, _ = mimetypes.guess_type(file_path)
    content_type = (
        content_type or 'application/octet-stream'
    )
    filename = (
        f"{book_file.book.title}_{book_file.format}"
        f".{book_file.format}"
    ).replace(' ', '_')

    response = FileResponse(
        open(file_path, 'rb'),
        content_type=content_type,
        as_attachment=True,
        filename=filename
    )

    # ── Increment counter & audit log ────────────
    token.use()
    DownloadLog.objects.create(
        token=token, user=request.user,
        ip_address=_get_ip(request),
        user_agent=request.META.get(
            'HTTP_USER_AGENT', ''),
        success=True
    )
    return response


@login_required
def library_redownload(request, purchased_id, fmt):
    """Re-download from My Library.
    No expiry — permanent access for owners.
    Creates a fresh 1-use token on demand."""
    purchased = get_object_or_404(
        PurchasedBook,
        id=purchased_id,
        user=request.user
    )
    book_file = get_object_or_404(
        purchased.book.files, format=fmt
    )

    # Fresh single-use token, valid 24 hours
    token = DownloadToken.objects.create(
        user=request.user,
        book_file=book_file,
        order=purchased.order,
        max_downloads=1,
        expires_at=timezone.now() + timedelta(hours=24)
    )
    return redirect(
        reverse('delivery:download', args=[str(token.token)])
    )


def _get_ip(request):
    """Extract real IP, handling proxies."""
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return (
        xff.split(',')[0].strip()
        if xff
        else request.META.get('REMOTE_ADDR')
    )


# Create your views here.
