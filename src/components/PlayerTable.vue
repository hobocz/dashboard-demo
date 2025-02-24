<script setup>

import { ref, onMounted } from 'vue'
import Vue3EasyDataTable from 'vue3-easy-data-table';
import 'vue3-easy-data-table/dist/style.css';
import PlayerOPSChart from './PlayerOPSChart.vue'


const rowsSelected = ref([]);
const defaultSortBy = "name_last";
const searchField = ["name_first", "name_last"];
const searchValue = ref("");
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

const getPlayerStats = async (index) => {
    const expandedItem = items.value[index];    
    if (!expandedItem.stats) {
        expandedItem.expandLoading = true;
        const response = await fetch(`http://127.0.0.1:8000/players/${items.value[index].id}/stats`)
        expandedItem.stats = await response.json()
        expandedItem.expandLoading = false
    }
}

</script>


<template>
    <div class="tableNotes">
    <span>Name search:&nbsp;</span>
    <input type="text" v-model="searchValue">
    <span id="headerNote">Select sorting available in the header</span>
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
        @expand-row="getPlayerStats"
        alternating
        buttons-pagination
        :rows-per-page=10
        :rows-items=[10,25]
        table-class-name="customize-table"
        >
            <template #empty-message>
                Loading...
            </template>
            <!-- <template #expand="item">
            <div>
                {{ item.stats }}
            </div>
            </template> -->
        </Vue3EasyDataTable>
    </div>
    <div class="tableNotes" v-if="rowsSelected.length > 10">
        No more than 10 players can be selected at once
    </div>
    <div v-else-if="rowsSelected.length > 0">
        <div class="tableNotes">Player OPS:</div>
        <div v-for="player in rowsSelected" :key="player.id" class="playerOPS">
            <PlayerOPSChart :player="player" />
        </div>
    </div>
</template>


<style scoped>
/* #tableContainer {
    max-height: 500px;
    overflow: scroll;
} */
.tableNotes {
    text-align: left;
    font-weight: bold;
    margin-top: .5em;
    margin-bottom: .5em;
}
#headerNote {
    float: right;
    font-size: small;
    font-style: italic;
}
.playerOPS {
    margin-bottom: .5em;
}
.customize-table {
    --easy-table-header-font-color: white;
    --easy-table-header-background-color: #BD9B60;
}
</style>