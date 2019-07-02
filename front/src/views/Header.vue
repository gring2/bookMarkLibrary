<template>
  <nav>
    <div>
      <div class="home-logo">
        <router-link :to="{name: 'home'}"  class="link-style-none">
          <h1>BookMarkLibrary</h1>
          </router-link>
      </div>
      <div>
        <ul class="list-style-none flex flex-items-center">
          <li>
            <router-link :to="{name: 'bookmarks'}"  class="manu">library</router-link>
          </li>

        </ul>
      </div>

    </div>


    <div class="authenticate flex-items-center" v-if="!isMobile">
      <div>
        <p>Hi! {{user? user.email : 'test email'}}</p>
      </div>
      <div class="logout-box">
        <Button className="logout"><template v-slot:text>Log out</template></Button>
      </div>
      <div class="">
        <router-link :to="{name: 'signup'}">
          <Button className="register"><template v-slot:text>Sign Up</template></Button>
        </router-link>
      </div>
      <div class="" v-if="!user">
        <router-link :to="{name: 'signin'}">
          <Button className="login"><template v-slot:text>Sign In</template></Button>
        </router-link>
      </div>
    </div>
  </nav>

</template>

<script lang="ts">
  import { Component, Prop, Vue } from 'vue-property-decorator'
  import Button from '@/components/Button.vue'
  import User from '@/vo/User'
  import {userMod} from '@/stores/modules/user'

@Component({
    components: {
      Button,
    },
  })
  export default class Header extends Vue {
     private user: User | null = userMod.user
     private isMobile: boolean = false;
     private testStr = 'test'

    calculateisMobile(){
      const html = document.querySelector('html')
      this.isMobile = html!.clientWidth < 768
    }
    
    signUp(){
      let dumm = new User()
      userMod.SIGN_UP(dumm)
    }

    mounted() {
      this.calculateisMobile()
      window.addEventListener('resize', this.calculateisMobile);
    }
  }
</script>

<style scoped lang="scss">
  @import "@/styles/header.scss";
</style>