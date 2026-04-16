from src.core.security import TokenManager
from src.services.account.auth.api_output import TokenModel
from src.services.account.refresh.api_input import IAPIRefreshToken

class RefreshTokensService:
    async def call(self, model: IAPIRefreshToken):
        user_id = TokenManager.id(model.refresh_token)
        access_token = TokenManager.access(user_id)
        refresh_token = TokenManager.refresh(user_id)
        return TokenModel(access_token=access_token, refresh_token=refresh_token)