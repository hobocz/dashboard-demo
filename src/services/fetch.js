import { usePlayerStore } from "@/stores/player"

const apiUrl = import.meta.env.VITE_API_URL
const posNames = {
    "1": "Pitcher",
    "2": "Catcher",
    "3": "1st Base",
    "4": "2nd Base",
    "5": "3rd Base",
    "6": "Shortstop",
    "7": "Left Field",
    "8": "Center Field",
    "9": "Right Field",
    "O": "Offence",
    "D": "Defense",
}

const mapPlayer = (player) => {
    return {
        id: player.id,
        name_first: player.name_first,
        name_last: player.name_last,
        name_use: `"${player.name_use}"`,
        team: player.team,
        birth_date: player.birth_date,
        height_total: `${player.height_feet}' - 
            ${player.height_inches != null ? player.height_inches : '?'}"`,
        weight: `${player.weight} lbs`,
        throws: player.throws,
        bats: player.bats,
        primary_position: `${player.primary_position ? player.primary_position
                + " - " + posNames[player.primary_position] : "undefined"}`
    }
}

export async function fetchData(type) {
    const playerStore = usePlayerStore()
    if (!["all", "batting", "pitching"].includes(type)) {
        playerStore.error = "Invalid player fetch type"
        return
    }
    if (type === "all" && playerStore.allPlayers) return
    if (type === "batting" && playerStore.battingOnly) return
    if (type === "pitching" && playerStore.pitchingOnly) return
    playerStore.loading = true
    try {
        const result = await fetch(`${apiUrl}/players/?stat=${type}`)
        const playerData = await result.json()
        if(type === "batting"){
            playerStore.battingOnly = playerData.map(mapPlayer)
        }
        else if(type === "pitching"){
            playerStore.pitchingOnly = playerData.map(mapPlayer)
        }
        else {
            playerStore.allPlayers = playerData.map(mapPlayer)
        }
    } catch (err) {
        playerStore.error = err
    } finally {
        playerStore.loading = false
    }
}