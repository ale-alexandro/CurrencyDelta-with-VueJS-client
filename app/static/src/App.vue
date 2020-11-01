<template>
  <div id="app">
    <h1> {{ delta }} </h1>
    <p>Выберите валюту 
    <select v-model="selected">
      <option v-for="currency in currencies" :value="currency.ID">{{ currency.Name }} ({{ currency.ISO_Char_Code }})</option>
    </select></p>
    <p>Начало промежутка времени <input type="date" min="1990-01-01" :max="currDate" v-model="startDate"/> {{ startDate_value }}</p>    
    <p>Конец промежутка времени <input type="date" min="1990-01-01" :max="currDate" v-model="endDate"/> {{ endDate_value }}</p>
    <div id="button" @click="getDelta()"> Запрос </div>
  </div>
</template>

<script>
import axios from 'axios'

function format(date) {
    var d = date.getDate();
    var m = date.getMonth() + 1;
    var y = date.getFullYear();
    return '' + (d <= 9 ? '0' + d : d) + '-' + (m<=9 ? '0' + m : m) + '-' + y;
}

export default {
  name: 'app',
  data () {
    return {
      currencies: [],
      selected: "none",
      startDate: format(new Date()),
      startDate_value: "",
      endDate: format(new Date()),
      endDate_value: "",
      currDate: format(new Date()),
      delta: ""
    }
  },
  created() {
    axios.get("/api/getCurrencyList").then(r => {
      this.currencies = r.data.data;
      this.selected = this.currencies[0].ID
    })
  },
  methods: {
    getFormatDate(date) {
      return new Date(date).getDate() + "-" + new Date(date).getMouth() + "-" + new Date.getFullYear();
    },
    getErrorText(data) {
      console.log(data);
      switch (data.error) {
        case 1: this.delta = "Ошибка: " + "Нет данных за " + data.date; break;
        case 2: this.delta = "Ошибка: " + "Не верно указана начальная дата ( " + data.date + ")"; break;
        case 3: this.delta = "Ошибка: " + "Не верно указана конечная дата ( " + data.date + ")"; break;
        case 4: this.delta = "Ошибка: " + "Валюты не существует ( " + data.cbr_cur_id + ")"; break;
      }
      console.log(this.delta)
    },
    getDelta() {
      this.delta = "Загружаю..."
      axios.get("/api/getCurrencyDelta?cur="+this.selected+"&start="+this.startDate+"&end="+this.endDate).then(r => {
          if (!(r.data.error)){
            this.delta = "Разница: " + r.data.delta + " Рублей";  
            this.startDate_value = r.data.start + " Рублей";
            this.endDate_value = r.data.end + " Рублей";
          } else {
            console.log("Handeling error " + r.data.error)
            this.getErrorText(r.data);
            this.startDate_value = "";
            this.endDate_value = "";
          }    
      }).catch(err => {this.delta = "Неизвестная ошибка"})
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  padding: 15px;
}

h1, h2 {
  font-weight: normal;
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

#button {
  background-color: #2c3e50; 
  color: white;
  transition: 0.3s;
  width: 150px;
  height: 30px;
  text-align: center;
  font-size: 24px;
}

#button:hover {
  background-color: #42b983;
  color: black;
  cursor: pointer;
}
</style>
