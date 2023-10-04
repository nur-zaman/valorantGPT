import random
import time

from colorama import Fore, Style
from g4f import BaseProvider, Provider, models


class freeGPT:
    WORKING_PROVIDERS = []

    def __init__(self,log=False) -> None:
        logging = log
        pass

    def get_providers(self) -> list[type[BaseProvider]]:
        provider_names = dir(Provider)
        ignore_names = [
            "annotations",
            "helper",
            "base_provider",
            "retry_provider",
            "BaseProvider",
            "AsyncProvider",
            "AsyncGeneratorProvider",
            "RetryProvider",
        ]
        return [
            getattr(Provider, provider_name)
            for provider_name in provider_names
            if not provider_name.startswith("__") and provider_name not in ignore_names
        ]


    def create_response(self,_provider: type[BaseProvider], prompt:str = "hello", role:str="user") -> str:
        model = models.gpt_35_turbo.name if _provider.supports_gpt_35_turbo else models.default.name
        response = _provider.create_completion(
            model=model,
            messages=[{"role": f"{role}", "content": f"{prompt}"}],
            stream=False,
        )
        return "".join(response)

    def test(self,_provider: type[BaseProvider]) -> bool:
        try:
            response = self.create_response(_provider)
            assert type(response) is str
            assert len(response) > 0
            return response
        except Exception as e:
            if self.logging:
                print(e)
            return False

    def update_working_providers(self):
        providers = self.get_providers()

        for _provider in providers:
            print(_provider)
            try:
                if _provider.__name__ in [
                    "Wewordle",
                ]:
                    continue
                if _provider.needs_auth:
                    continue

                start_time = time.time()  # Record the start time
                if _provider.working:
                    print("Provider:", _provider.__name__)
                    result = self.test(_provider)
                    print("Result:", result)
                    if not result:
                        continue
                    else:
                        end_time = time.time()  # Record the end time
                        duration = end_time - start_time  # Calculate duration
                        print(
                            f"Response from {_provider.__name__} took {duration} seconds !"
                        )
                        self.WORKING_PROVIDERS.append(_provider)
            except AttributeError:
                pass
        print(f"Working Providers: {self.WORKING_PROVIDERS}")

        print()

    def update_working_providers_from_name(self, providers):
        all_providers = self.get_providers()
        for _provider in all_providers:
            try:
                if _provider.__name__ in providers:
                    self.WORKING_PROVIDERS.append(_provider)
            except AttributeError:
                pass

        print(self.WORKING_PROVIDERS)

    def try_all_working_providers(self, prompt, role="user"):
        providers = self.WORKING_PROVIDERS
        random.shuffle(providers)
        for _provider in providers:
            print("Trying ", _provider.__name__)
            start_time = time.time()  # Record the start time
            try:
                response = self.create_response(_provider, prompt, role=role)
                if len(response) > 0:
                    end_time = time.time()  # Record the end time
                    duration = end_time - start_time  # Calculate duration
                    print(f"Response from {_provider.__name__} took {duration} seconds")
                    return response
            except Exception as e:
                print(e)
                continue
