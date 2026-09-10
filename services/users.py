from database.repositories.users import UserRepository

class UserService:
    @staticmethod
    def register_user(user_id: int, full_name: str = "", username: str = "") -> None:
        UserRepository.register(user_id=user_id, full_name=full_name, username=username)

    @staticmethod
    def get_broadcast_user_ids() -> list[int]:
        return UserRepository.get_broadcast_ids()

    @staticmethod
    def mark_user_blocked(user_id: int) -> None:
        UserRepository.mark_blocked(user_id)

    @staticmethod
    def get_users_count() -> int:
        return UserRepository.get_count()
