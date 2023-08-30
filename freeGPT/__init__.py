from g4f import BaseProvider, models, Provider



class freeGPT:
    WORKING_PROVIDERS =[]

    def __init__(self) -> None:
        pass

    def get_providers(self) -> list[type[BaseProvider]]:
        provider_names = dir(Provider)
        ignore_names = [
            "base_provider",
            "BaseProvider"
        ]
        provider_names = [
            provider_name
            for provider_name in provider_names
            if not provider_name.startswith("__") and provider_name not in ignore_names
        ]
        return [getattr(Provider, provider_name) for provider_name in sorted(provider_names)]


    def create_response(self,_provider: type[BaseProvider],prompt='Hello') -> str:
        if _provider.supports_gpt_35_turbo:
            model = models.gpt_35_turbo.name    
        elif _provider.supports_gpt_4:
            model = models.gpt_4
        elif hasattr(_provider, "model"):
            model = _provider.model
        else:
            model = None
        response = _provider.create_completion(
            model=model,
            messages=[{"role": "user", "content": f"{prompt}"}],
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
            return False
    def update_working_providers(self):
        providers = self.get_providers()

        for _provider in providers:
            if _provider.__name__ in ['ChatgptLogin','Opchatgpts','Lockchat','You','Acytoo']:
                continue
            if _provider.needs_auth:
                continue
            print("Provider:", _provider.__name__)
            result = self.test(_provider)
            print("Result:", result)
            if _provider.working and not result:
                pass
            else:
                self.WORKING_PROVIDERS.append(_provider)
        print(f"Working Providers: {self.WORKING_PROVIDERS}")

        print()
    def try_all_working_providers(self,prompt):
        for _provider in self.WORKING_PROVIDERS:
            try:
                response = self.create_response(_provider,prompt)
                if len(response) > 0:
                    return response
            except Exception as e:
                continue



