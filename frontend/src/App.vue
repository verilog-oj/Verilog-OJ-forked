<template>
  <div id="app" style="top: 0px; left: 0px">
    <el-menu
      :default-active="this.$route.path"
      mode="horizontal"
      v-bind:router="true"
      id="nav"
    >
      <el-menu-item index="/" id="title">{{ school }}</el-menu-item>
      <el-menu-item index="/">
        <i class="el-icon-star-off"></i>主页</el-menu-item
      >
      <el-menu-item index="/problempage/1">
        <i class="el-icon-menu"></i>题目</el-menu-item
      >
      <el-menu-item index="/statue">
        <i class="el-icon-tickets"></i>状态</el-menu-item
      >
      <!-- <el-menu-item index="/contest">
        <i class="el-icon-bell"></i>Contest</el-menu-item> -->

      <el-button round id="button" @click="registeropen" v-show="!loggedIn"
        >注册</el-button
      >
      <el-button round id="button" @click="loginopen" v-show="!loggedIn"
        >登录</el-button
      >

      <el-dropdown
        id="user"
        v-show="loggedIn"
        @click="showHome"
        @command="handleCommand"
        :show-timeout="100"
        split-button
      >
        <span class="el-dropdown-link">Welcome, {{ username }}</span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="home">个人主页</el-dropdown-item>
          <!-- <el-dropdown-item command="submittion">Submittion</el-dropdown-item> -->
          <el-dropdown-item command="setting">设置</el-dropdown-item>
          <!-- <el-dropdown-item command="classes" divided>班级</el-dropdown-item> -->
          <el-dropdown-item command="admin" divided v-show="isSuperUser"
            >管理</el-dropdown-item
          >
          <el-dropdown-item command="logout" divided>注销</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </el-menu>

    <register ref="registerdialog"></register>

    <login ref="logindialog"></login>

    <el-backtop :bottom="50">
      <div
        style="
           {
            height: 100%;
            width: 100%;
            background-color: #f2f5f6;
            box-shadow: 0 0 6px rgba(0, 0, 0, 0.12);
            text-align: center;
            line-height: 40px;
            color: #1989fa;
          }
        "
      >
        UP
      </div>
    </el-backtop>
    <!-- >  主体<-->
    <transition name="el-fade-in-linear" mode="out-in">
      <router-view id="route"></router-view>
    </transition>
    <!-- >  主体<-->
    <div class="footer">
      Copyright © 2022-{{ currentYear }} verilog.fun. Powered by <a href="https://github.com/YAVGroup/Verilog-OJ" target="_blank">Verilog-OJ</a>.
            遵守 AGPLv3 许可证开放<a href="https://github.com/verilog-oj/Verilog-OJ-forked" target="_blank">源码</a>
    </div>
  </div>
</template>

<script>


import Cookies from "js-cookie";
import { mapState } from "vuex";

export default {
  name: "App",
  components: {
    login: (resolve) => require(["@/login"], resolve),
    register: (resolve) => require(["@/register"], resolve),
  },
  data() {
    return {
      school: "UCAS",
      currentYear: 2024,
    };
  },
  computed: mapState(["loggedIn", "userID", "username", "isSuperUser"]),
  methods: {
    year() {
      return this.currentYear ? this.currentYear.getFullYear() : 2024;
    },
    loginopen() {
      this.$refs.logindialog.open();
    },
    registeropen() {
      this.$refs.registerdialog.open();
    },
    showHome: function () {
      this.$router.push({
        name: "user",
        params: { userid: this.userID },
      });
    },
    getCurrentYear() {
      const date = new Date();
      this.currentYear = date;
    },
    handleCommand(command) {
      if (command == "logout") {
        this.$axios
          .get("/user/logout/")
          .then((response) => {
            this.$store.commit({
              type: "logOut",
            });
            this.$message({
              message: "登出成功！",
              type: "success",
            });
          })
          .catch((error) => {
            this.$message.error(
              "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
            );
          });
      }
      if (command == "home") {
        this.showHome();
      }
      if (command == "setting") {
        this.$router.push({
          name: "setting",
          params: { username: this.username },
        });
      }
      if (command == "admin") {
        this.$router.push({
          name: "admin",
        });
      }
    },
  },
};
</script>

<style scope>
.el-dropdown-link {
  cursor: pointer;
  color: #409eff;
}
#button {
  float: right;
  margin: 10px;
}
#user {
  float: right;
  margin: 10px;
}
#nav {
  background-color: #ffffff;
  position: relative;
  left: 0px;
  top: 0px;
  z-index: 5;
  width: 100%;
  /* box-shadow: 00px 0px 00px rgb(255, 255, 255),
    0px 0px 10px rgb(255, 255, 255),
     0px 0px 0px rgb(255, 255, 255),
     1px 1px 0px rgb(218, 218, 218);  */
}
#route {
  position: relative;
  top: 10px;
}
#title {
  font-size: 20px;
  font-weight: bold;
}
.el-row {
  margin-bottom: 20px;
}
.footer {
  margin-top: 20px;
  margin-bottom: 10px;
  text-align: center;
  font-size: small;
  color: #777;
}
</style>
