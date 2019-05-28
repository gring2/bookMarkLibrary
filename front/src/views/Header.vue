<template>
  <nav>
    <div>
      <div class="home-logo">
        <a  class="link-style-none"
        ><h1>BookMarkLibrary</h1></a>

      </div>
      <div>
        <ul class="list-style-none flex flex-items-center">
          <li><a class="manu">library</a></li>

        </ul>
      </div>

    </div>


    <div class="authenticate flex-items-center">
      <div>
        <p>Hi! {{email}}</p>
      </div>
      <div class="logout-box">
        <Button className="logout"><template v-slot:text>Log out</template></Button>
      </div>
      <div class="">

        <Button className="register"><template v-slot:text>Sign Up</template></Button>
      </div>
      <div class="">

        <Button className="login"><template v-slot:text>Sign In</template></Button>
      </div>
    </div>
  </nav>

</template>

<script lang="ts">
  import { Component, Prop, Vue } from 'vue-property-decorator';
  import Button from '@/components/Button'
  @Component({
    components: {
      Button,
    },
  })
  export default class Header extends Vue {
     @Prop({default: 'email'}) private email!: string;
  }
</script>

<style scoped lang="scss">
  @import "@/styles/header.scss"
</style>