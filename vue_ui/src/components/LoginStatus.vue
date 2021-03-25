<template>
  <div class="LoginStatus">
    <h2>Login Status</h2>
    <ul>
      <li>user: {{user}}</li>
      <li>active: {{active}}</li>
      <li>authenticated: {{authenticated}}</li>
    </ul>
    <pre>
    {{info}}
    </pre>
    <h2> Login/Logout </h2>
    <button v-if="user == null" v-on:click="handle_login()">Login</button>
    <button v-else v-on:click="handle_logout()">Logout</button>
    <p>
    End
    </p>

  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.headers.post['X-Requested-With']='XMLHttpRequest'

export default {
  name: 'LoginStatus',
  props: { },
  data: function(){ 
    return {
      user: null,
      active: false,
      authenticated: false,
      info: ''
    }
  },
  methods:{
    set_state: function(state){
      this.info = state
      this.user = state.user
      this.active = state.active
      this.authenticated = state.authenticated
    },

    handle_logout: function(){ 
      axios({
        method: 'post',
        url:  'http://127.0.0.1:5000/logout',
        withCredentials: true,
        data: {}})
      .then(response => { this.set_state(response.data) })
    },

    handle_login: function() {
      this.$gAuth
        .getAuthCode()
        .then((authCode) => {
          axios({
            method: 'post',
            url:  'http://127.0.0.1:5000/auth_code',
            withCredentials: true,
            data: {code: authCode, redirect_uri: 'postmessage'}})
          .then(response => { this.set_state(response.data) })
        })
        .catch((error) => {
          this.info = error
        });
    }
  },
  mounted () {
    axios
      .get('http://127.0.0.1:5000/auth_status', {withCredentials: true})
      .then(response => {
        this.info = response.data
        this.user = response.data.user
        this.active = response.data.active
        this.authenticated = response.data.authenticated
      })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h2 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
