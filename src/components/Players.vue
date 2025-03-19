<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useFetchPlayersStore } from "@/services/fetch"
import { AgGridVue } from "ag-grid-vue3"
import { AllCommunityModule, ModuleRegistry, themeBalham } from "ag-grid-community"
ModuleRegistry.registerModules([AllCommunityModule])


const apiUrl = import.meta.env.VITE_API_URL
// Get/create player data pinia store
const fetchPlayersStore = useFetchPlayersStore()
// Vue Router related data
const route = useRoute()
const router = useRouter()
// AG Grid related data
const playerGridRef = ref(null)
const autoSizeStrategy = {
    type: "fitGridWidth"
}
const rowSelection = { 
    mode: "singleRow" ,
    checkboxes: false,
    enableClickSelection: true
}
const playerColumnDefs = ref([
    { field: "name_first", headerName: "First Name" },
    { field: "name_last", headerName: "Last Name", filter: true },
    { field: "name_use", headerName: "Use Name" },
    { field: "team", headerName: "Team", filter: true },
    { field: "birth_date", headerName: "Birth Date", filter: true },
    { field: "height_total", headerName: "Height" },
    { field: "weight", headerName: "Weight" },
    { field: "throws", headerName: "Throws", filter: true },
    { field: "bats", headerName: "Bats", filter: true },
    { field: "primary_position", headerName: "Primary Pos", filter: true },
])
const battingColumnDefs = ref([
    { field: "year", headerName: "YR", headerTooltip: "Year" },
    { field: "league", headerName: "LG", headerTooltip: "League" },
    { field: "org_abbreviation", headerName: "ORG", headerTooltip: "Org Abbreviation" },
    { field: "plate_appearances", headerName: "PA", headerTooltip: "Plate Appearances" },
    { field: "at_bats", headerName: "AB", headerTooltip: "At Bats" },
    { field: "games", headerName: "G", headerTooltip: "Games" },
    { field: "games_started", headerName: "GS", headerTooltip: "Games Started" },
    { field: "runs", headerName: "R", headerTooltip: "Runs" },
    { field: "hits", headerName: "H", headerTooltip: "Hits" },
    { field: "doubles", headerName: "2B", headerTooltip: "Doubles" },
    { field: "triples", headerName: "3B", headerTooltip: "Triples" },
    { field: "home_runs", headerName: "HR", headerTooltip: "Home Runs" },
    { field: "bases_on_balls", headerName: "BB", headerTooltip: "Bases on Balls" },
    { field: "strikeouts", headerName: "K", headerTooltip: "Strikeouts" },
    { field: "sacrifices", headerName: "SH", headerTooltip: "Sacrifices" },
    { field: "sacrifice_flies", headerName: "SF", headerTooltip: "Sacrifice Flies" },
    { field: "stolen_bases", headerName: "SB", headerTooltip: "Stolen Bases" },
    { field: "caught_stealing", headerName: "CS", headerTooltip: "Caught Stealing" },
])
const selectedPlayer = ref(null)
const selectedPlayerStats = ref(null)


onMounted(() => {
    fetchPlayersStore.fetchData("all")
})
const fetchPlayerStats = async (pid) => {
    const response = await fetch(`${apiUrl}/players/${pid}/stats`)
    selectedPlayerStats.value = await response.json()
}
// Respond to AG Grid's selection-changed event.
const onSelectionChanged = () => {
    selectedPlayerStats.value = playerGridRef.value.api.getSelectedRows()
    selectedPlayer.value = selectedPlayerStats.value[0]
    fetchPlayerStats(selectedPlayer.value.id)
}
// Use the player IDs as row IDs
const getRowId = (params) => { 
    return params.data.id.toString()
}
</script>

<template>
    <div class="componentContainer">
        <div class="border border-secondary border-2 rounded-1">
            <AgGridVue
                ref="playerGridRef"
                :rowData="fetchPlayersStore.playersAll"
                :columnDefs="playerColumnDefs"
                :autoSizeStrategy="autoSizeStrategy"
                :pagination="true"
                :paginationPageSize="25"
                :paginationPageSizeSelector="[25, 50, 100]"
                :theme="themeBalham"
                :rowSelection="rowSelection" 
                @selection-changed="onSelectionChanged"
                :getRowId="getRowId"
                style="height: 400px"
            >
            </AgGridVue>
        </div>
        <div>
            <div class="alert alert-danger" v-show="fetchPlayersStore.error">{{ fetchPlayersStore.error }}</div>
            <div class="fw-bold m-1" v-show="!selectedPlayer">Select a player to see their stats...</div>
        </div>
        <div id="statContainer">
            <div v-if="selectedPlayer" class="h4 mt-2 text-decoration-underline">
                {{ selectedPlayer.name_first + " " + selectedPlayer.name_last }}
            </div>
            <div v-if="selectedPlayer">
                <div v-if="selectedPlayerStats.batting?.length > 0"
                    class="border border-secondary border-2 rounded-1 m-1 p-1">
                    <div>Batting Stats:</div>
                    {{ selectedPlayerStats.batting }}
                    <AgGridVue
                        :rowData="fetchPlayersStore.playersAll"
                        :columnDefs="battingColumnDefs"
                        :autoSizeStrategy="autoSizeStrategy"
                        :theme="themeBalham"
                        :getRowId="getRowId"
                    >
                    </AgGridVue>
                </div>
                <div v-else class="border border-secondary border-2 rounded-1 m-1 p-1 bg-warning bg-opacity-25">
                    Player has no batting stats
                </div>
                <div v-if="selectedPlayerStats.pitching?.length > 0"
                    class="border border-secondary border-2 rounded-1 m-1 p-1">
                    <div>Pitching Stats:</div>
                    {{ selectedPlayerStats.pitching }}
                </div>
                <div v-else class="border border-secondary border-2 rounded-1 m-1 p-1 bg-warning bg-opacity-25">
                    Player has no pitching stats
                </div>
            </div>
        </div> 
    </div>
</template>

<style scoped>

</style>