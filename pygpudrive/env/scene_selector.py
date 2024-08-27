import random
import os
from math import ceil
from pygpudrive.env.config import SelectionDiscipline


def select_scenes(config):
    """Selects a number of traffic scenes from the data directory based on the specified discipline.

    Args:
        config: Data configuration object containing the path to the data directory and the selection discipline.

    Raises:
        ValueError: If the data directory does not exist or is empty.
        ValueError: If the data directory does not contain any traffic scenes.

    Returns:
        _type_: _description_
    """
    assert os.path.exists(config.path) and os.listdir(
        config.path
    ), "The data directory does not exist or is empty."

    all_scenes = sorted(os.listdir(config.path))
    selected_scenes = None
    if not any(scene.startswith("tfrecord") for scene in all_scenes):
        raise ValueError(
            "The data directory does not contain any traffic scenes. Maybe you specified a path to the wrong folder?"
        )

    def random_sample(k):
        rand = random.Random(0x5CA1AB1E)
        return rand.sample(all_scenes, k)

    def repeat_to_N(scenes):
        repeat_count = ceil(config.num_scenes / len(scenes))
        return (scenes * repeat_count)[: config.num_scenes]

    match config.discipline:
        case SelectionDiscipline.FIRST_N:
            selected_scenes = all_scenes[: config.num_scenes]
            selected_scenes = all_scenes[: config.num_scenes]
        case SelectionDiscipline.RANDOM_N:
            selected_scenes = random_sample(all_scenes)
        case SelectionDiscipline.PAD_N:
            selected_scenes = repeat_to_N(all_scenes)
        case SelectionDiscipline.EXACT_N:
            assert len(all_scenes) == config.num_scenes
            selected_scenes = all_scenes
        case SelectionDiscipline.K_UNIQUE_N:
            assert (
                config.k_unique_scenes > 0
            ), "K_UNIQUE_N discipline requires specifying positive value for K"
            selected_scenes = repeat_to_N(
                random_sample(config.k_unique_scenes)
            )

    if not any(scene.startswith("tfrecord") for scene in selected_scenes):
        raise ValueError(
            "The selected scene is not a traffic scenario. Something went wrong with the scene selection. Please check your data path."
        )

    return [
        os.path.join(os.path.abspath(config.path), selected_scene)
        for selected_scene in selected_scenes
    ]
