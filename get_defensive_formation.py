
import pandas as pd

# Load datasets
players_df = pd.read_csv("data/players.csv")
plays_df = pd.read_csv("data/plays.csv")
player_play_df = pd.read_csv("data/player_play.csv")

# Identify Defensive Players
def get_defensive_players(plays_df, player_play_df, players_df):
    # Merge player play data with general play info
    merged_df = player_play_df.merge(
        plays_df[['gameId', 'playId', 'defensiveTeam', 'pff_passCoverage', 'pff_manZone']],
        on=['gameId', 'playId'],
        how='left'
    )
    
    # Merge with player positions
    merged_df = merged_df.merge(players_df[['nflId', 'position']], on='nflId', how='left')
    
    # Keep only defensive players (teamAbbr == defensiveTeam)
    defensive_players = merged_df[merged_df["teamAbbr"] == merged_df["defensiveTeam"]]

    return defensive_players

# Classify Defensive Players into DL, LB, DB
def classify_defensive_formation(defensive_players):
    formation_labels = []

    for (gameId, playId), play_group in defensive_players.groupby(['gameId', 'playId']):
        # Count position groups
        dl_count = sum(play_group["position"].isin(["DE", "DT", "NT", "EDGE"]))  # Defensive Linemen
        lb_count = sum(play_group["position"].isin(["MLB", "OLB", "ILB"]))  # Linebackers
        db_count = sum(play_group["position"].isin(["CB", "S", "FS", "SS"]))  # Defensive Backs
        
        # Count blitzing players
        blitz_count = sum(play_group["wasInitialPassRusher"] == 1)

        # Determine base formation
        if db_count == 4:
            if dl_count == 4 and lb_count == 3:
                formation = "4-3 Defense"
            elif dl_count == 3 and lb_count == 4:
                formation = "3-4 Defense"
        elif db_count == 5:
            formation = "Nickel"
        elif db_count == 6:
            if lb_count == 2:
                formation = "Dime (3-2-6)"
            else:
                formation = "Dime"
        elif db_count >= 7:
            formation = "Prevent"
        elif dl_count >= 5:
            formation = "Goal Line"
        else:
            formation = "Unknown"

        # Add coverage scheme
        coverage_scheme = play_group["pff_passCoverage"].iloc[0]
        man_zone = play_group["pff_manZone"].iloc[0]

        formation_labels.append({
            "gameId": gameId,
            "playId": playId,
            "defensiveFormation": formation,
            "blitzCount": blitz_count,
            "coverageScheme": coverage_scheme,
            "manZone": man_zone
        })

    return pd.DataFrame(formation_labels)

defensive_players = get_defensive_players(plays_df, player_play_df, players_df)
defensive_formations = classify_defensive_formation(defensive_players)

# Merge With Play Data
plays_df = plays_df.merge(defensive_formations, on=["gameId", "playId"], how="left")

# Save Data
plays_df.to_csv("data/plays_with_defensive_formations.csv", index=False)

print(plays_df.head())
