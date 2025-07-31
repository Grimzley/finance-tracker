def get_category_icon(category):
    return {
        'salary': 'bi-cash',
        'freelance': 'bi-laptop',
        'investment': 'bi-graph-up',
        'gift': 'bi-gift',
        'inc_other': 'bi-three-dots',

        'food': 'bi-fork-knife',
        'bills': 'bi-house-exclamation-fill',
        'transport': 'bi-luggage-fill',
        'shopping': 'bi-cart-fill',
        'entertainment': 'bi-joystick',
        'health': 'bi-heart-pulse-fill',
        'savings': 'bi-piggy-bank-fill',
        'exp_other': 'bi-three-dots',
    }.get(category, 'bi-question-circle')

def get_category_color(category):
    return {
        'salary': 'text-success',
        'freelance': 'text-primary',
        'investment': 'text-info',
        'gift': 'text-info',
        'inc_other': 'text-secondary',

        'food': 'text-warning',
        'bills': 'text-danger',
        'transport': 'text-muted',
        'shopping': 'text-secondary',
        'entertainment': 'text-primary',
        'health': 'text-danger',
        'savings': 'text-success',
        'exp_other': 'text-muted',
    }.get(category, 'text-muted')

def get_category_description(category):
    return {
        'food': 'Groceries, dining out, coffee shops, and snacks.',
        'bills': 'Monthly recurring expenses like utilities, rent, and subscriptions.',
        'transport': 'Costs related to getting around.',
        'shopping': 'Non-essential purchases and personal items.',
        'entertainment': 'Leisure activities and events.',
        'health': 'Medical and wellness-related expenses.',
        'savings': 'Money intentionally set aside or transferred to savings.',
        'exp_other': 'Anything that doesn’t fit into the main categories.',
    }.get(category, 'Budget Category')
