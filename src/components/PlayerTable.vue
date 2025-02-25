<script setup>

import { ref, onMounted, watch } from 'vue'
import Vue3EasyDataTable from 'vue3-easy-data-table';
import 'vue3-easy-data-table/dist/style.css';
import PlayerBattingChart from './PlayerBattingChart.vue'


const rowsSelected = ref([]);
const defaultSortBy = "name_last";
const searchField = ["name_first", "name_last"];
const searchValue = ref("");
const clearInput = () => {
    searchValue.value = '';
};
const headers = [
    // { text: "ID", value: "id" },
    { text: "First Name", value: "name_first" },
    { text: "Last Name", value: "name_last", sortable: true },
    { text: "Use Name", value: "name_use" },
    { text: "Team", value: "team", sortable: true },
    { text: "Birth Date", value: "birth_date" },
    { text: "Height", value: "height_total"},
    { text: "Weight", value: "weight" },
    { text: "Throws", value: "throws" },
    { text: "Bats", value: "bats" },
    { text: "Primary Pos", value: "primary_position", sortable: true },
];
const items = ref([])
const posNames = {
    1: "Pitcher",
    2: "Catcher",
    3: "1st Base",
    4: "2nd Base",
    5: "3rd Base",
    6: "Shortstop",
    7: "Left Field",
    8: "Center Field",
    9: "Right Field",
    "O": "Offence",
    "D": "Defense",
}
const battingChartRef = ref(null);

onMounted(async () => {
    const response = await fetch("http://127.0.0.1:8000/players/")
    const playerData = await response.json()
    items.value = playerData.map((player) => {
        return {
            id: player.id, 
            name_first: player.name_first,
            name_last: player.name_last,
            name_use: `"${player.name_use}"`,
            team: player.team,
            birth_date: player.birth_date,
            height_total: `${player.height_feet}' - ${player.height_inches ? player.height_inches : '?'}"`,
            weight: `${player.weight} lbs`,
            throws: player.throws,
            bats: player.bats,
            primary_position: `${player.primary_position ? player.primary_position + " - " + posNames[player.primary_position] : "undefined"}`,
        }
    })
})

watch(rowsSelected, (updatedRows) => {
    // Watch Vue3EasyDataTable's rowsSelected and update the child component on change.
    battingChartRef.value.selectedPlayers = updatedRows
}, { deep: true })

</script>


<template>
    <div id="compContainer">
        <div class="tableNotes vspace">
            <span>Name search:&nbsp;</span>
            <input type="text" v-model="searchValue">
            <span @click="clearInput" id="clearButton">Clear</span>
            <span id="headerNote">Select sorting available in the table header</span>
        </div>
        <div id="tableContainer">    
            <Vue3EasyDataTable
            v-model:items-selected="rowsSelected"
            hide-header-selection
            :table-min-height=80
            :headers="headers"
            :items="items"
            :sort-by="defaultSortBy"
            :search-field="searchField"
            :search-value="searchValue"
            alternating
            buttons-pagination
            :rows-per-page=10
            :rows-items=[10,25]
            table-class-name="customize-table"
            >
                <template #empty-message>
                    Loading...
                </template>
            </Vue3EasyDataTable>
        </div>
        
        <div v-if="rowsSelected.length > 5" class="tableNotes">
            No more than 5 players can be queried at once
        </div>
        <div v-else class="tableNotes">Select up to 5 players to compare OPS by year</div>
        <div v-show="rowsSelected.length > 0" id="chartContainer">
            <PlayerBattingChart ref="battingChartRef" />
        </div>
    </div>
</template>


<style scoped>
#compContainer{
    padding-left: 1rem;
    padding-right: 1rem;
}
#tableContainer {
    border: 4px solid #BD9B60;
    border-radius: 5px;
}
#chartContainer {
    min-height: 200px;
    height: 300px;
}
.tableNotes {
    text-align: left;
    font-weight: bold;
    margin-top: .5em;
    margin-bottom: .5em;
}
.vspace {
    padding-top: 1em;;
}
#headerNote {
    float: right;
    font-size: small;
    font-style: italic;
}
#clearButton{
    margin-left: .5em;
    font-size: small;
    background-color: lightgray;
    color: black;
    padding: .3em;
    border-radius: 5px;
}
#clearButton:hover {
    cursor: pointer;
}
.playerOPS {
    margin-bottom: .5em;
}
.customize-table {
    --easy-table-border: 1px solid #BD9B60;
    --easy-table-header-font-color: white;
    --easy-table-header-background-color: #BD9B60;
}
</style>