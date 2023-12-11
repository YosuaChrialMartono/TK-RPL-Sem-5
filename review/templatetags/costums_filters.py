from django import template

register = template.Library()

@register.filter
def average_rating(reviews):
    total_ratings = sum([review.rating for review in reviews])
    num_reviews = len(reviews)
    return round(total_ratings / num_reviews, 2) if num_reviews > 0 else 0.0