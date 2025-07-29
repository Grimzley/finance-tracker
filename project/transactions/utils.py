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
