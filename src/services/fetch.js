import { defineStore } from "pinia"
import { ref } from "vue"


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

export const useFetchPlayerStore = defineStore("fetchStore", () => {
    const allPlayers = ref(null)
    const playersBatting = ref(null)
    const playersPitching = ref(null)
    const error = ref(null)
    const loading = ref(false)

    async function fetchData(type) {
        if (!["all", "batting", "pitching"].includes(type)) {
            error.value = "Invalid fetch type"
            return
        }
        // Should data be reloaded each time?...
        // if (type === "all" && allPlayers.value) return
        // if (type === "batting" && playersBatting.value) return
        // if (type === "pitching" && playersPitching.value) return
        loading.value = true
        try {
            const result = await fetch(`${apiUrl}/players/?stat=${type}`)
            const playerData = await result.json()
            playersBatting.value = playerData.map(mapPlayer)
        } catch (err) {
            error.value = err
        } finally {
            loading.value = false
        }

    }

    return { allPlayers, playersBatting, playersPitching, error, loading, fetchData }
})