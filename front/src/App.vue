<template>
  <div id="app">
    <Header ></Header>
    <router-view/>
  </div>
</template>


<script lang="ts">
  import { Component, Vue } from 'vue-property-decorator'
  import Header from '@/views/Header.vue' // @ is an alias to /src
  import User from '@/vo/User'
  import { mapState } from 'vuex'
@Component({
    components: {
      Header,
    },
  })

export default class App extends Vue {
}
</script>

<style lang="scss">
  @import '@/styles/init.scss';
  #app {
      font-family: 'Avenir', Helvetica, Arial, sans-serif;
      height: 100%
  }

</style>
