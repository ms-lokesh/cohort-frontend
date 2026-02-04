from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import get_resolver


@require_http_methods(['GET'])
def list_urls(request):
    """Return a JSON list of loaded URL patterns (for debugging deployed routing)."""
    try:
        resolver = get_resolver(None)
        patterns = []
        for p in resolver.url_patterns:
            try:
                patterns.append(str(p.pattern))
            except Exception:
                patterns.append(repr(p))

        return JsonResponse({'routes': patterns})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
