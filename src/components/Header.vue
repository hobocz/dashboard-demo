<script setup>

import { ref } from 'vue'
const showNotes = ref(false)

</script>


<template>
    <div id="header">
        <div id="leftSide">Header content can be added...</div>
        <div id="rightSide"> Please read --> <span id="notesButton" @click="showNotes = !showNotes">Toggle Page Notes</span></div>
    </div>
    <div v-show="showNotes" id="notesBox">
        Only Batting stats are shown. Could be pitching too
        TODO - Player has no batting stats
    </div>
</template>


<style scoped>

#header {
    background: hsla(240, 9%, 98%, 0.5);
    font-weight: bold;
    width: 100%;
    height: 3em;
    display: flex;
    justify-content: space-between;
}
#leftSide {
    padding: .5em;
}
#rightSide {
    padding: .5em;
    justify-content: flex-end;
}
#notesButton{
    margin-left: .5em;
    font-size: small;
    background-color: lightgray;
    color: black;
    padding: .3em;
    border-radius: 5px;
    margin: .5em;
}
#notesBox {
    margin-left: 1em;
    margin-right: 1em;
    margin-bottom: 1em;
    padding: .5em;
    background-color: white;
    color: black;
    text-align: left;
}
#notesButton:hover {
    cursor: pointer;
}

</style>