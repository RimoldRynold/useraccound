from django.urls import path
from .views import add_scraped_users, get_next_user, get_init_data, get_text, get_tokens, should_scrape, log_result, log_dup_result, mark_dead, add_bulk_token 

app_name = "api"

urlpatterns = [
    path('add-scraped', add_scraped_users, name='add_scraped_user'),
    path('get-next-user', get_next_user, name='get_next_user'),
    path('get-init-data', get_init_data, name='get_init_data'),
    path('get-text', get_text, name='get_text'),
    path('get-tokens', get_tokens, name='get_token'),
    path('should-scrape', should_scrape, name='should_scrape'),
    path('log-result', log_result, name='log_result'),
    path('log-dup-result', log_dup_result, name='log_dup_result'),
    path('mark-dead', mark_dead, name='mark_dead'),
    path('add-bulk-token', add_bulk_token, name='add_bulk_token')
]
