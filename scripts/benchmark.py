import gpudrive
from sim_utils.create import SimCreator
# Create an instance of RewardParams
reward_params = gpudrive.RewardParams()
reward_params.rewardType = gpudrive.RewardType.DistanceBased  # Or any other value from the enum
reward_params.distanceToGoalThreshold = 1.0  # Set appropriate values
reward_params.distanceToExpertThreshold = 1.0  # Set appropriate values

# Create an instance of Parameters
params = gpudrive.Parameters()
params.polylineReductionThreshold = 0.5  # Set appropriate value
params.observationRadius = 10.0  # Set appropriate value
params.datasetInitOptions = gpudrive.DatasetInitOptions.FirstN
params.rewardParams = reward_params  # Set the rewardParams attribute to the instance created above

# Now use the 'params' instance when creating SimManager
sim = gpudrive.SimManager(
    exec_mode=gpudrive.madrona.ExecMode.CPU,
    gpu_id=0,
    num_worlds=1,
    auto_reset=True,
    json_path="/home/aarav/gpudrive/valid_nocturne",
    params=params
)

print(sim.controlled_state_tensor().to_torch().shape)

