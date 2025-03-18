<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from 'vue-router'
import PlayerBattingOPSChart from "./PlayerBattingOPSChart.vue"
import { useFetchPlayerStore } from '@/services/fetch'
import { AgGridVue } from "ag-grid-vue3"
import { AllCommunityModule, ModuleRegistry, themeBalham } from 'ag-grid-community'
ModuleRegistry.registerModules([AllCommunityModule])


const fetchPlayerStore = useFetchPlayerStore()
// Vue Router related data
const route = useRoute()
const router = useRouter()
// AG Grid related data
const gridRef = ref(null)
const autoSizeStrategy = {
    type: 'fitGridWidth'
}
const rowSelection = { 
    mode: 'multiRow' ,
    headerCheckbox: false,
}
const selectionColumnDef = {
    sortable: true,
    resizable: false,
    width: 60
}
const columnDefs = ref([
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
const rowData = ref(null)
// Reference to the exposed child data
const battingChartRef = ref(null)
const selectCount = ref(0)

onMounted(() => {
    fetchPlayerStore.fetchData("batting")
})
// This event fires when grid data changes. Since the grid loads itself
// async, we need to wait for this before we can tick checkboxes
const onRowDataUpdated = () => {
    const loadedRows = gridRef.value.api.getDisplayedRowCount()
    if (loadedRows > 0){
        if (route.query.pids) {
            const pids = route.query.pids
            .split(',')
            .map((idStr) => parseInt(idStr))
            .filter((num) => !isNaN(num))
            pids.forEach(id => {
                const node = gridRef.value.api.getRowNode(id.toString())
                if (node) { node.setSelected(true) }
            })
        }
    }
}
// Respond to AG Grid's selection-changed event. Updates the selected
// players in the child component and the current URL
const onSelectionChanged = () => {
    const selectedRows = gridRef.value.api.getSelectedRows()
    selectCount.value = selectedRows.length
    battingChartRef.value.selectedPlayers = selectedRows

    let playerIDs = []
    selectedRows.forEach(player => {
        playerIDs.push(player.id)
    })
    router.replace({
        name: 'batting',
        query: {
        ...route.query,
        pids: playerIDs.join(","),
        },
    })
}
// Use the player IDs as row IDs
const getRowId = (params) => { 
    return params.data.id.toString()
}
</script>

<template>
    <div class="componentContainer">
        <div id="tableContainer">
            <AgGridVue
                ref="gridRef"
                :rowData="fetchPlayerStore.playersBatting"
                :columnDefs="columnDefs"
                :autoSizeStrategy="autoSizeStrategy"
                :pagination="true"
                :paginationPageSize="25"
                :paginationPageSizeSelector="[25, 50, 100]"
                :theme="themeBalham"
                :rowSelection="rowSelection" 
                @selection-changed="onSelectionChanged"
                :selectionColumnDef="selectionColumnDef"
                :getRowId="getRowId"
                @row-data-updated="onRowDataUpdated"
                style="height: 400px"
            >
            </AgGridVue>
        </div>
        <div>
            <div class="tableNotes" v-show="selectCount === 0">Select players to compare some stats...</div>
            <div v-show="selectCount > 0">
                <button class="btn btn-secondary btn-sm p-0" @click="gridRef.api.deselectAll">Clear Selections</button>
            </div>
        </div>
        <div id="chartContainer" v-show="selectCount > 0">
            <PlayerBattingOPSChart ref="battingChartRef" />
        </div> 
    </div>
</template>

<style scoped>
.componentContainer{
    padding-left: 1em;
    padding-right: 1em;
    margin-bottom: 3em;
}
#tableContainer {
    border: .2em solid gray;
    border-radius: 5px;
}
#chartContainer {
    min-height: 200px;
    height: 300px;
}
.tableNotes {
    text-align: left;
    font-weight: bold;
    margin: .2em;
}
.clearButton {
    margin-left: auto;
}
</style>