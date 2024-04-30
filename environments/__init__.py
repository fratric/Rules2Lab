#this file is here to implment fnctions for environment registration
#not sure if it is really need, see https://github.com/microsoft/CyberBattleSim/blob/main/cyberbattle/__init__.py
from gymnasium.envs.registration import register
from gymnasium.envs.registration import registry

#when you import environments package, you can register all your environments here

if 'Prolog-Gym/DataSharingEnv-v0' in registry:
     registry.pop('Prolog-Gym/DataSharing-v0')
register(
     id="Prolog-Gym/DataSharing-v0",
     entry_point="environments.dataSharing:DataSharing",
     max_episode_steps=10,
)


#register(
#     id="environments/multinational_transaction_env-v0",
#     entry_point="environments.multinational_transaction_env:MultinationalTransactionEnv",
#     max_episode_steps=400,
#)