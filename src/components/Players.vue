<script setup>
import { ref, onMounted } from "vue"
import { fetchData } from "@/services/fetch"
import { usePlayerStore } from "@/stores/player"
import { AgGridVue } from "ag-grid-vue3"
import { AllCommunityModule, ModuleRegistry, themeBalham } from "ag-grid-community"
ModuleRegistry.registerModules([AllCommunityModule])


const apiUrl = import.meta.env.VITE_API_URL
const playerStore = usePlayerStore()
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
const gridThemeCustom = themeBalham.withParams({
    // headerTextColor: "white",
    headerBackgroundColor: "#dddddd",
});
const battingColumnDefs = ref([
    { field: "year", headerName: "YR", headerTooltip: "Year", flex: 4, minWidth: 45 },
    { field: "league", headerName: "LG", headerTooltip: "League", flex: 2, minWidth: 32 },
    { field: "org_abbreviation", headerName: "ORG", headerTooltip: "Org Abbreviation", flex: 3, minWidth: 45 },
    { field: "plate_appearances", headerName: "PA", headerTooltip: "Plate Appearances", flex: 3, minWidth: 32 },
    { field: "at_bats", headerName: "AB", headerTooltip: "At Bats", flex: 3, minWidth: 32 },
    { field: "games", headerName: "G", headerTooltip: "Games", flex: 3, minWidth: 32 },
    { field: "games_started", headerName: "GS", headerTooltip: "Games Started", flex: 3, minWidth: 32 },
    { field: "runs", headerName: "R", headerTooltip: "Runs", flex: 3, minWidth: 32 },
    { field: "hits", headerName: "H", headerTooltip: "Hits", flex: 3, minWidth: 32 },
    { field: "doubles", headerName: "2B", headerTooltip: "Doubles", flex: 2, minWidth: 32 },
    { field: "triples", headerName: "3B", headerTooltip: "Triples", flex: 2, minWidth: 32 },
    { field: "home_runs", headerName: "HR", headerTooltip: "Home Runs", flex: 2, minWidth: 32 },
    { field: "bases_on_balls", headerName: "BB", headerTooltip: "Bases on Balls", flex: 2, minWidth: 32 },
    { field: "strikeouts", headerName: "K", headerTooltip: "Strikeouts", flex: 3, minWidth: 32 },
    { field: "sacrifices", headerName: "SH", headerTooltip: "Sacrifices", flex: 1, minWidth: 32 },
    { field: "sacrifice_flies", headerName: "SF", headerTooltip: "Sacrifice Flies", flex: 1, minWidth: 32 },
    { field: "stolen_bases", headerName: "SB", headerTooltip: "Stolen Bases", flex: 2, minWidth: 32 },
    { field: "caught_stealing", headerName: "CS", headerTooltip: "Caught Stealing", flex: 2, minWidth: 32 },
])
const pitchingColumnDefs = ref([
    { field: "year", headerName: "YR", headerTooltip: "Year", flex: 4, minWidth: 45 },
    { field: "league", headerName: "LG", headerTooltip: "League", flex: 2, minWidth: 32 },
    { field: "org_abbreviation", headerName: "ORG", headerTooltip: "Org Abbreviation", flex: 3, minWidth: 45 },
    { field: "games", headerName: "G", headerTooltip: "Games", flex: 2, minWidth: 32 },
    { field: "games_started", headerName: "GS", headerTooltip: "Games Started", flex: 1, minWidth: 32 },
    { field: "complete_games", headerName: "CG", headerTooltip: "Complete Games", flex: 1, minWidth: 32 },
    { field: "games_finished", headerName: "GF", headerTooltip: "Games Finished", flex: 2, minWidth: 32 },
    { field: "innings_pitched", headerName: "IP", headerTooltip: "Innings Pitched", flex: 3, minWidth: 32 },
    { field: "wins", headerName: "W", headerTooltip: "Wins", flex: 2, minWidth: 32 },
    { field: "losses", headerName: "L", headerTooltip: "Losses", flex: 2, minWidth: 32 },
    { field: "saves", headerName: "SV", headerTooltip: "Saves", flex: 2, minWidth: 32 },
    { field: "total_batters_faced", headerName: "BF", headerTooltip: "Total Batters Faced", flex: 3, minWidth: 32 },
    { field: "at_bats", headerName: "AB", headerTooltip: "At Bats", flex: 3, minWidth: 32 },
    { field: "hits", headerName: "H", headerTooltip: "Hits", flex: 2, minWidth: 32 },
    { field: "doubles", headerName: "2B", headerTooltip: "Doubles", flex: 2, minWidth: 32 },
    { field: "triples", headerName: "3B", headerTooltip: "Triples", flex: 2, minWidth: 32 },
    { field: "home_runs", headerName: "HR", headerTooltip: "Home Runs", flex: 2, minWidth: 32 },
    { field: "bases_on_balls", headerName: "BB", headerTooltip: "Bases on Balls", flex: 2, minWidth: 32 },
    { field: "strikeouts", headerName: "K", headerTooltip: "Strikeouts", flex: 2, minWidth: 32 },
])
const battingRowData = ref(null)
const pitchingRowData = ref(null)
const selectedPlayer = ref(null)
const selectedPlayerStats = ref(null)


onMounted(() => {
    playerGridRef.value.api.setGridOption("alwaysShowHorizontalScroll", true)
    fetchData("all")
})

const mapBattingData = () => {
    return selectedPlayerStats.value.batting.map((stat) => {
        return {
            id: stat.id,
            year: stat.year,
            league: stat.league,
            org_abbreviation: stat.org_abbreviation,
            plate_appearances: stat.plate_appearances,
            at_bats: stat.at_bats,
            games: stat.games,
            games_started: stat.games_started,
            runs: stat.runs,
            hits: stat.hits,
            doubles: stat.doubles,
            triples: stat.triples,
            home_runs: stat.home_runs,
            bases_on_balls: stat.bases_on_balls,
            strikeouts: stat.strikeouts,
            sacrifices: stat.sacrifices,
            sacrifice_flies: stat.sacrifice_flies,
            stolen_bases: stat.stolen_bases,
            caught_stealing: stat.caught_stealing,
        }
    })
}
const mapPitchingData = () => {
    return selectedPlayerStats.value.pitching.map((stat) => {
        return {
            id: stat.id,
            year: stat.year,
            league: stat.league,
            org_abbreviation: stat.org_abbreviation,
            games: stat.games,
            games_started: stat.games_started,
            complete_games: stat.complete_games,
            games_finished: stat.games_finished,
            innings_pitched: stat.innings_pitched,
            wins: stat.wins,
            losses: stat.losses,
            saves: stat.saves,
            total_batters_faced: stat.total_batters_faced,
            at_bats: stat.at_bats,
            hits: stat.hits,
            doubles: stat.doubles,
            triples: stat.triples,
            home_runs: stat.home_runs,
            bases_on_balls: stat.bases_on_balls,
            strikeouts: stat.strikeouts,
        }
    })
}
const fetchPlayerStats = async (pid) => {
    const response = await fetch(`${apiUrl}/players/${pid}/stats`)
    selectedPlayerStats.value = await response.json()
    battingRowData.value = mapBattingData()
    pitchingRowData.value = mapPitchingData()
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
                :rowData="playerStore.allPlayers"
                :columnDefs="playerStore.playerColumnDefs"
                :autoSizeStrategy="autoSizeStrategy"
                :pagination="true"
                :paginationPageSize="25"
                :paginationPageSizeSelector="[25, 50, 100]"
                :theme="gridThemeCustom"
                :rowSelection="rowSelection" 
                @selection-changed="onSelectionChanged"
                :getRowId="getRowId"
                style="height: 400px"
            >
            </AgGridVue>
        </div>
        <div>
            <div class="alert alert-danger" v-show="playerStore.error">{{ playerStore.error }}</div>
            <div class="fw-bold m-1" v-show="!selectedPlayer">Select a player to see their stats...</div>
        </div>
        <div id="statContainer">
            <div v-if="selectedPlayer" class="h4 mt-2 fw-bold text-decoration-underline">
                {{ selectedPlayer.name_first + " " + selectedPlayer.name_last }}
            </div>
            <div v-if="selectedPlayer">
                <div v-if="selectedPlayerStats.batting?.length > 0"
                    class="border border-secondary border-2 rounded-1 my-2 p-1">
                    <div class="p-1 fw-bold">Batting Stats:</div>
                    <AgGridVue
                        ref="battingGridRef"
                        :rowData="battingRowData"
                        :columnDefs="battingColumnDefs"
                        :autoSizeStrategy="autoSizeStrategy"
                        :theme="gridThemeCustom"
                        :getRowId="getRowId"
                        domLayout="autoHeight"
                    >
                    </AgGridVue>
                </div>
                <div v-else class="border border-secondary border-2 rounded-1 my-2 p-1 bg-warning bg-opacity-25">
                    Player has no batting stats
                </div>
                <div v-if="selectedPlayerStats.pitching?.length > 0"
                    class="border border-secondary border-2 rounded-1 my-2 p-1">
                    <div class="p-1 fw-bold">Pitching Stats:</div>
                    <AgGridVue
                        ref="pitchingGridRef"
                        :rowData="pitchingRowData"
                        :columnDefs="pitchingColumnDefs"
                        :autoSizeStrategy="autoSizeStrategy"
                        :theme="gridThemeCustom"
                        :getRowId="getRowId"
                        domLayout="autoHeight"
                    >
                    </AgGridVue>
                </div>
                <div v-else class="border border-secondary border-2 rounded-1 my-2 p-1 bg-warning bg-opacity-25">
                    Player has no pitching stats
                </div>
            </div>
        </div> 
    </div>
</template>

<style scoped>

</style>