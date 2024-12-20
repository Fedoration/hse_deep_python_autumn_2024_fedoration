from classes import (
    RegularAttributes,
    SlotsAttributes,
    WeakrefAttributes,
    measure_creation_time,
    measure_access_time,
)


def main():
    num_objects = 1_000_000

    creation_times = {"Regular": [], "Slots": [], "Weakref": []}
    access_times = {"Regular": [], "Slots": [], "Weakref": []}

    for _ in range(10):  # 10 прогонов
        # Regular
        creation_time, created_objects = measure_creation_time(
            RegularAttributes, num_objects
        )
        access_time = measure_access_time(created_objects)
        creation_times["Regular"].append(creation_time)
        access_times["Regular"].append(access_time)

        # Slots
        creation_time_slots, created_objects_slots = measure_creation_time(
            SlotsAttributes, num_objects
        )
        access_time_slots = measure_access_time(created_objects_slots)
        creation_times["Slots"].append(creation_time_slots)
        access_times["Slots"].append(access_time_slots)

        # Weakref
        creation_time_weakref, created_objects_weakref = measure_creation_time(
            WeakrefAttributes, num_objects
        )
        access_time_weakref = measure_access_time(created_objects_weakref)
        creation_times["Weakref"].append(creation_time_weakref)
        access_times["Weakref"].append(access_time_weakref)

    # Усредненные результаты
    for mode in creation_times:
        avg_creation_time = sum(creation_times[mode]) / len(creation_times[mode])
        avg_access_time = sum(access_times[mode]) / len(access_times[mode])
        print(f"{mode} (усреднённые результаты):")
        print(f"  Время создания: {avg_creation_time:.6f} сек")
        print(f"  Время чтения/изменения: {avg_access_time:.6f} сек")


if __name__ == "__main__":
    main()
