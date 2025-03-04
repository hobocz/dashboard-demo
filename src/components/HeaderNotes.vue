<script setup>
import { ref } from 'vue'
const showNotes = ref(false)
</script>

<template>
    <div id="header">
        <span id="notesButton" @click="showNotes = !showNotes">
            {{ showNotes ? "Toggle Notes Off" : "Toggle Notes On" }}
        </span>
    </div>
    <div v-show="showNotes" id="notes">
        <div class="notes-section">Notes:</div>
        Since the data load is relatively small, all players are loaded 
        into the table. <span class="italic">This is just the player data, not the 
        batting/pitching stats.</span><br/><br/>
        <div class="notes-section">Component Usage:</div>
        <ul>
            <li>All columns are sortable.</li>
            <li>Text based filtering is enabled on appropriate columns. 
                Unfortunately select/checkbox filtering is an enterprise 
                (paid) option.</li>
            <li>Use the checkboxes to select players. Players' 
                OPS-by-year will be compared in a chart.</li>
            <li>NOTE: The OPS calculation does not include HBP as this 
                was not included in the original data. Also the assumption 
                was made that singles could be calculated by:
                1B = H - 2B - 3B - HR</li>
        </ul>
        <div class="notes-section top-space">Todos:</div>
        <ul>
            <li>Currently only OPS comparisons are implemented. Many 
                other batting and pitching stats could be compared in 
                the same way.</li>
                <li>If a player has no batting stats, currently a simple 
                alert box is fired, however the checkbox remains checked. This
                needs to be programatically unchecked. <br/>
                For now, the user must uncheck that player
                manually.
            </li>
        </ul>
    </div>
</template>

<style scoped>
#header {
    width: 100%;
    display: flex;
    justify-content: flex-end;
}
#notesButton{
    margin: .5em;
    font-size: small;
    font-weight: bold;
    background-color: lightgray;
    color: black;
    padding: .2em;
    border-radius: 5px;
    cursor: pointer;
}
#notes {
    background-color: lightgray;
    color: black;
    border: 2px solid black;
    text-align: left;
    padding: .2em;
}
.notes-section {
    font-weight: bold;
}
.warning {
    font-weight: bold;
    color: red;
}
.italic {
    font-style: italic;
}
</style>