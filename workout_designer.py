import pandas as pd
import random

# Normalize text
df['Level'] = df['Level'].str.strip().str.lower()
df['Goal'] = df['Goal'].str.strip().str.lower()
df['Muscle'] = df['Muscle'].str.strip().str.lower()

def estimate_level():
    print("\n----------------------------")
    print(" FITNESS LEVEL ESTIMATION")
    print("----------------------------")
    pushups = int(input(" Max push-ups in one set: "))
    pullups = int(input(" Max pull-ups in one set: "))
    plank = int(input(" Max plank hold (seconds): "))
    squats = int(input(" Max bodyweight squats in one set: "))

    levels = [
        "zero_strength","beginner","pro_beginner",
        "intermediate","pro_intermediate","almost_advanced","advanced_elite"
    ]

    # Convert raw numbers to levels
    push_level = min(len(levels)-1, pushups // 15)
    pull_level = min(len(levels)-1, pullups // 5)
    core_level = min(len(levels)-1, plank // 30)
    leg_level  = min(len(levels)-1, squats // 20)

    all_levels = [push_level, pull_level, core_level, leg_level]
    avg_level = sum(all_levels) / len(all_levels)

    # Adjustment logic: pull extremes toward the middle
    adjusted_levels = []
    for l in all_levels:
        if l > avg_level + 1:   # very strong compared to avg
            adjusted_levels.append(l - 1)
        elif l < avg_level - 1: # very weak compared to avg
            adjusted_levels.append(l + 1)
        else:
            adjusted_levels.append(l)

    final_level_index = round(sum(adjusted_levels) / len(adjusted_levels))
    final_level_index = max(0, min(final_level_index, len(levels)-1))  # clamp to valid range

    print("\n Results by category:")
    print(f" - Push: {levels[push_level]}")
    print(f" - Pull: {levels[pull_level]}")
    print(f" - Core: {levels[core_level]}")
    print(f" - Legs: {levels[leg_level]}")
    print(f"\n Smart Adjusted Levels (numeric): {adjusted_levels}")
    print(f" Final Smart Estimate Level: {levels[final_level_index].upper()}")
    print("----------------------------\n")

    return levels[final_level_index]

# -------------------------
# Generate weekly workout
# -------------------------
def generate_plan(level, goal):
    week_plan = {
        "Day 1": "Push",
        "Day 2": "Pull",
        "Day 3": "Legs",
        "Day 4": "Core",
        "Day 5": "Full Body",
        "Day 6": "Push + Core",
        "Day 7": "Active Recovery"
    }

    print("\n===================================")
    print("       WEEKLY WORKOUT PLAN")
    print("===================================\n")

    for day, muscle in week_plan.items():
        print(f"{day} - {muscle}")
        print("-" * 30)

        if muscle == "Active Recovery":
            print(" - Walk, stretch, or yoga\n")
            continue

        muscles = [m.strip().lower() for m in muscle.split("+")]
        for m in muscles:
            exercises = df[(df["Level"] == level) & (df["Goal"] == goal) & (df["Muscle"] == m)]
            if exercises.empty:
                print(f" - No {m} exercises found for this level/goal.\n")
            else:
                chosen = exercises.sample(min(3, len(exercises)))  # up to 3 exercises per muscle
                for _, row in chosen.iterrows():
                    print(f" - {row['Exercise']} ({row['Sets']}x{row['Reps']} rest {row['Rest']}s) → {row['Notes']}")
        print()

# -------------------------
# Main
# -------------------------
print("===================================")
print("   CALISTHENICS WORKOUT DESIGNER")
print("===================================\n")

level = input("Do you know your level? (y/n): ").strip().lower()

if level == "y":
    level = input(" Enter level (zero_strength, beginner, pro_beginner, intermediate, pro_intermediate, almost_advanced, advanced_elite): ").strip().lower()
else:
    level = estimate_level()

goal = input("\nWhat is your goal? (strength / endurance / hypertrophy / fat_loss): ").strip().lower()

generate_plan(level, goal)
