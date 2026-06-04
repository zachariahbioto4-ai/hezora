import os
import re

print("🚀 Starting BookBase Platform Automated Updates...")

# --- 1. ENFORCE AUTHENTICATION ON CHECKOUT ---
orders_view_path = 'orders/views.py'
if os.path.exists(orders_view_path):
    with open(orders_view_path, 'r') as f:
        content = f.read()
    
    # Check if login_required is imported, if not add it
    if 'login_required' not in content:
        content = "from django.contrib.auth.decorators import login_required\n" + content
    
    # Try to safely patch a function-based checkout view
    if 'def checkout' in content and '@login_required' not in content:
        content = re.sub(r'(def checkout\(.*?\):)', r'@login_required(login_url="/accounts/login/")\n\1', content)
        with open(orders_view_path, 'w') as f:
            f.write(content)
        print("✅ Added @login_required decorator to Checkout view.")
    
    # Try to safely patch a class-based checkout view
    elif 'class CheckoutView' in content and 'LoginRequiredMixin' not in content:
        if 'LoginRequiredMixin' not in content:
            content = "from django.contrib.auth.mixins import LoginRequiredMixin\n" + content
        content = re.sub(r'(class CheckoutView\()(.*?\):)', r'\1LoginRequiredMixin, \2', content)
        with open(orders_view_path, 'w') as f:
            f.write(content)
        print("✅ Added LoginRequiredMixin to Checkout CBV.")
else:
    print("⚠️  Could not find orders/views.py. Ensure your checkout view has login protection.")


# --- 2. ADD CATEGORY FILTERING LOGIC ---
books_view_path = 'books/views.py'
if os.path.exists(books_view_path):
    with open(books_view_path, 'r') as f:
        content = f.read()
    
    # Look for a standard ListView get_queryset method to patch
    if 'def get_queryset' in content and 'request.GET.get(' not in content:
        patch = """
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)"""
        
        # Simple injection if standard return exists
        content = re.sub(r'(return queryset)', f'{patch}\n        \\1', content)
        with open(books_view_path, 'w') as f:
            f.write(content)
        print("✅ Added Category filtering logic to Books view.")
else:
    print("⚠️  Could not find books/views.py to inject category filtering.")


# --- 3. GENERATE HTML UI COMPONENTS ---
os.makedirs('templates/components', exist_ok=True)

# A. Dynamic Profile Avatar Component (Handles Unregistered, Initial Letter, & Custom Image)
avatar_html = """
<a href="{% url 'accounts:profile' %}" class="profile-btn" style="text-decoration: none;">
    {% if request.user.is_authenticated %}
        {% if request.user.avatar %}
            <img src="{{ request.user.avatar.url }}" alt="Profile" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 2px solid #e5e7eb;">
        {% else %}
            <div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #3b82f6); color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2rem; text-transform: uppercase;">
                {{ request.user.first_name|default:request.user.username|make_list|first }}
            </div>
        {% endif %}
    {% else %}
        <div style="width: 40px; height: 40px; border-radius: 50%; background: #f3f4f6; color: #9ca3af; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; border: 1px solid #e5e7eb;">
            <svg fill="currentColor" viewBox="0 0 24 24" style="width: 20px; height: 20px;"><path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
        </div>
    {% endif %}
</a>
"""
with open('templates/components/navbar_avatar.html', 'w') as f:
    f.write(avatar_html)

# B. Profile Settings Update Form Snippet (For custom image uploads)
settings_form_html = """
<form method="POST" action="{% url 'accounts:profile_update' %}" enctype="multipart/form-data">
    {% csrf_token %}
    <div class="form-group">
        <label>Upload Profile Image</label>
        <input type="file" name="avatar" accept="image/*" class="form-control">
    </div>
    <button type="submit" class="btn btn-primary">Save Changes</button>
</form>
"""
with open('templates/components/profile_settings_form.html', 'w') as f:
    f.write(settings_form_html)

# C. Discovery Button Component
discovery_html = """
{% if request.path != '/' and request.path != '/dashboard/' %}
    <a href="{% url 'books:dashboard' %}" class="btn btn-outline-primary discovery-btn">
        <svg style="width: 16px; height: 16px; margin-right: 5px;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        Discovery
    </a>
{% endif %}
"""
with open('templates/components/discovery_btn.html', 'w') as f:
    f.write(discovery_html)

# D. Empty Orders / Empty Category State
empty_state_html = """
<div class="empty-state" style="text-align: center; padding: 50px 20px; background: #f9fafb; border-radius: 12px; margin-top: 20px;">
    <svg style="width: 64px; height: 64px; color: #9ca3af; margin: 0 auto 15px auto;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path></svg>
    <h3 style="color: #374151; font-size: 1.2rem; margin-bottom: 10px;">Nothing to see here yet!</h3>
    <p style="color: #6b7280; margin-bottom: 20px;">There are no books currently matching this criteria in the database.</p>
    <a href="{% url 'books:dashboard' %}" class="btn btn-primary" style="background: #3b82f6; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none;">Explore Books</a>
</div>
"""
with open('templates/components/empty_state.html', 'w') as f:
    f.write(empty_state_html)

print("✅ Successfully generated UI components in `templates/components/`")
print("🎉 Updates Complete!")
