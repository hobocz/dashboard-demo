import { ref } from "vue"
import { defineStore } from "pinia"


export const usePlayerStore = defineStore("players", () => {
    const allPlayers = ref(null)
    const battingOnly = ref(null)
    const pitchingOnly = ref(null)
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

    return { 
        allPlayers, 
        battingOnly, 
        pitchingOnly, 
        error, 
        loading,
        playerColumnDefs
    }
})