from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import LibraryEntry
from books.serializers import BookSerializer

class LibraryViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        entries = LibraryEntry.objects.filter(user=request.user).select_related('book')
        books = [entry.book for entry in entries]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_book(self, request):
        book_id = request.data.get('book_id')
        entry, created = LibraryEntry.objects.get_or_create(user=request.user, book_id=book_id)
        return Response({'status': 'added' if created else 'already exists'})

    @action(detail=False, methods=['delete'])
    def remove_book(self, request):
        book_id = request.data.get('book_id')
        LibraryEntry.objects.filter(user=request.user, book_id=book_id).delete()
        return Response({'status': 'removed'})


@require_POST
@login_required
def add_book_view(request):
    book_id = request.POST.get('book_id')
    if book_id:
        LibraryEntry.objects.get_or_create(user=request.user, book_id=book_id)
    return redirect(request.META.get('HTTP_REFERER', '/library/'))


@require_POST
@login_required
def remove_book_view(request):
    book_id = request.POST.get('book_id')
    if book_id:
        LibraryEntry.objects.filter(user=request.user, book_id=book_id).delete()
    return redirect('/library/')
