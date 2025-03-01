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
            <li>You can search for players by name. Both first name 
                and last name are searched.</li>
            <li>Sorting is available on select columns. (Hover the 
                column header) </li>
            <li>Use the checkboxes to select up to 5 players. Players' 
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
            <li>Filtering table columns.</li>
            <li>Possibly replace the table altogether. Not sure I like 
                this one.</li>
            <li>Tons of other things :)</li>
        </ul>
        <div class="notes-section top-space">Issues:</div>
        <ul>
            <li>If a player has no batting stats, currently a simple 
                alert box is fired. However the checkbox remains checked 
                and the player remains in the chart. These need to both be 
                removed. <br/><span class="italic">For now, unchecking that player manually 
                will create the correct state.</span>
            </li>
            <li>
                <span class="warning">!!!</span> Please avoid the "select all" 
                checkbox in the table header. Since we have 1200+ rows, this 
                causes the browser to hang for a few seconds. Data is not retrieved
                for any number of players beyond 5, so the network traffic is avoided.
                There does not appear to be a way to remove this checkbox outside of
                editing the source code. (one of the reasons I'm not sold on this 
                table implementation)
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
}
#notesButton:hover {
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