from clean_logger.application.use_cases.create_order import CreateOrderUseCase


class FakeLogger:
    def __init__(self):
        self.messages = []

    def info(self, message, **ctx):
        self.messages.append(
            ("INFO", message, ctx)
        )

    debug = warning = error = info

def test_logs_order_created():
    logger = FakeLogger()

    use_case = CreateOrderUseCase(logger)
    use_case.execute("123")

    assert logger.messages[0][1] == "Creating order"