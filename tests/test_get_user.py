from app.check_users import get_user_by_id



def test_find_correct_user_by_id():
    user_read = get_user_by_id(1)
    user_dict = user_read.model_dump()
    assert user_dict["id"] == 1


def test_find_incorrect_user():
    result = get_user_by_id(-1)
    assert result is None