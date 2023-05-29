# 单例模式，实例内存一致
class driver:
    _instance = None
    driver1 = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def quit(cls):
        if cls.driver1 is None:
            pass
        else:
            cls.driver1.quit()
            cls.driver1 = None
            cls._instance = None