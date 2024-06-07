from gymnasium.envs.registration import register
from gymnasium.envs.registration import registry

#when you import environments package, you can register all your environments here

if 'environments/DataSharing-v0' in registry:
     registry.pop('environments/DataSharing-v0')
register(
     id="environments/DataSharing-v0",
     entry_point="environments.dataSharing:DataSharing",
     max_episode_steps=50,
     disable_env_checker=False
)


#register(
#     id="environments/multinational_transaction_env-v0",
#     entry_point="environments.multinational_transaction_env:MultinationalTransactionEnv",
#     max_episode_steps=400,
#)