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

export const useFetchPlayersStore = defineStore("fetchPlayers", () => {
    const playersAll = ref(null)
    const playersBatting = ref(null)
    const playersPitching = ref(null)
    const error = ref(null)
    const loading = ref(false)
    const playerColumnDefs = ref([
        { field: "name_first", headerName: "First Name", flex: 3, minWidth: 80 },
            { field: "name_last", headerName: "Last Name", filter: true, flex: 3, minWidth: 95 },
            { field: "name_use", headerName: "Use Name", flex: 3, minWidth: 80 },
            { field: "team", headerName: "Team", filter: true, flex: 2, minWidth: 65 },
            { field: "birth_date", headerName: "Birth Date", filter: true, flex: 3, minWidth: 95 },
            { field: "height_total", headerName: "Height", flex: 2, minWidth: 55 },
            { field: "weight", headerName: "Weight", flex: 2, minWidth: 60 },
            { field: "throws", headerName: "Throws", filter: true, flex: 1, minWidth: 75 },
            { field: "bats", headerName: "Bats", filter: true, flex: 1, minWidth: 60 },
            { field: "primary_position", headerName: "Primary Pos", filter: true, flex: 3, minWidth: 100 },
        ])

    async function fetchData(type) {
        if (!["all", "batting", "pitching"].includes(type)) {
            error.value = "Invalid player fetch type"
            return
        }
        if (type === "all" && playersAll.value) return
        if (type === "batting" && playersBatting.value) return
        if (type === "pitching" && playersPitching.value) return
        loading.value = true
        try {
            const result = await fetch(`${apiUrl}/players/?stat=${type}`)
            const playerData = await result.json()
            if(type === "batting"){
                playersBatting.value = playerData.map(mapPlayer)
            }
            else if(type === "pitching"){
                playersPitching.value = playerData.map(mapPlayer)
            }
            else {
                playersAll.value = playerData.map(mapPlayer)
            }
        } catch (err) {
            error.value = err
        } finally {
            loading.value = false
        }

    }

    return { playersAll, 
        playersBatting, 
        playersPitching, 
        error, 
        loading, 
        playerColumnDefs, 
        fetchData
    }
})