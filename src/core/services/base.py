from sqlalchemy.ext.asyncio import AsyncSession

class BaseService:
    """ 
    A basic service that simply has a session
    """
    def __init__(self, session: AsyncSession):
        self.session = session