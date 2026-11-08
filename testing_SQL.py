from datetime import date
from pprint import pprint

from SQL import (
    get_match_history_last_three_years,
    count_fixtures_before_date,
    get_all_available_players,
    count_partnership_matches
)


def test(function, *parameters):
    print("Function:", function.__name__)
    print("Parameters:", parameters)

    try:
        result = function(*parameters)

        if isinstance(result, list):
            print(f"Returned (showing first {min(3, len(result))} of {len(result)}):")
            pprint(result[:3], sort_dicts=True)

        else:
            print("Data:", result)

    except Exception as err:
        print("Error:", err)

    print()


# Get Match History Last Three Years
test(get_match_history_last_three_years, 6, date(2026, 11, 8))
test(get_match_history_last_three_years, 25, date(2026, 11, 8))
test(get_match_history_last_three_years, 6, date(2026, 11, 8))
test(get_match_history_last_three_years, 6, date(2026, 3, 18))


# Count Fixtures Before Date
test(count_fixtures_before_date, 2, date(2026, 11, 8))
test(count_fixtures_before_date, 1, date(2026, 11, 8))
test(count_fixtures_before_date, 2, date(2025, 9, 19))


# Get All Available Players
test(get_all_available_players, 1)
test(get_all_available_players, 99999)
test(get_all_available_players, 1)


# Count Partnership Matches
test(count_partnership_matches, 6, 5)
test(count_partnership_matches, 1, 7)
test(count_partnership_matches, 5, 6)