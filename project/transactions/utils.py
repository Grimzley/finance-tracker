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
        'freelance': 'text-palette-grey',
        'investment': 'text-palette-blue',
        'gift': 'text-palette-pink',
        'inc_other': 'text-palette-five',

        'food': 'text-palette-five',
        'bills': 'text-palette-teal',
        'transport': 'text-palette-brown',
        'shopping': 'text-palette-grey',
        'entertainment': 'text-palette-orange',
        'health': 'text-palette-red',
        'savings': 'text-palette-pink',
        'exp_other': 'text-palette-five',
    }.get(category, 'text-palette-five')

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
