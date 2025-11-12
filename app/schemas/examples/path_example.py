from typing import Any

PathExample: dict[str, dict[str, Any]] = {
    'normal': {
        'summary': 'A normal example',
        'description': 'A **normal** item works correctly.',
        'value': {
            'pickup': {
                'lat': 12.1234567,
                'lng': 123.1234567,
            },
            'dropoff': [
                {
                    'lat': 12.1234567,
                    'lng': 123.1234567,
                },
                {
                    'lat': 12.1234567,
                    'lng': 123.1234567,
                },
            ],
        },
    },
}
