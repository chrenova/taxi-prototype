function init(){

  Vue.component('week-days-tab', {
    props: ['weekDay'],
    template: `
    
    <li class="nav-item active">
    <a  class="nav-link active" data-toggle="tab"
    v-bind:href="weekDay.id"
    role="tab"
    aria-controls="{{weekDay.id}}"
    v-if:aria-selected="{true:weekDay.active}" >{{weekDay.day}}</a>
    </li>
    `
  });
  
  Vue.component('tasks-per-day', {
    props: ['weekDay'],
    template: `
             <table class="table table-bordered table-hover">
                <thead class="thead-light">
                  <tr>
                    <th scope="col">Vytvorená</td>
                    <th scope="col">Odkiaľ</th>
                    <th scope="col">Kam</th>
                    <th scope="col">Poznámka</th>
                    <th scope="col">Čas na vybavenie</th>
                    <th scope="col">Navrhovaná cena</th>
                    <th scope="col">Priradené</th>
                    <th scope="col">Stav</th>
                    <th scope="col">&nbsp;</th>
                  </tr>
                </thead>
                <tbody v-bind:id="weekDay.id+'-tasks'" >
                  <tr v-for="task in weekDay.tasks">
                      <th scope="row">{{task.created}}</th>
                      <td>{{task.from}}</td>
                      <td>{{task.to}}</td>
                      <td style="white-space:pre" class="koment">{{task.comment}}</td>
                      <td>{{task.timetoFix}}</td>
                      <td>{{task.offeredPrice}}</td>
                      <td>{{task.driver}}</td>
                      <td class="nezacala">{{task.status}}</td>
                      <td>
                          <div class="btn-group-vertical">
                              <button type="submit" class="btn btn-default btn-md" data-toggle="modal" data-target="#editOrderModal">Edituj</button>
                          </div>
                      </td>
                  </tr>
                  
                </tbody>
            </table>
          <div>
        </div>
    `
  });

  return new Vue({
    el: '#app',
    data: {
      task: [
        {
          id:1,
          day: "Pondelok",
          active:true,
          tasks:[
            {
             created: '29 Sep 2017 22:03:47',
              from:'Hviezdoslavova',
              to:'Kalvaria',
              comment:'Nieco tu bude',
              timetoFix:'10',
              offeredPrice:'2.5',
              driver:'Fero',
              status:'Nezacala'
            }
          ]
        },
        {
          id:2,
          day: "Utorok",
          active:false,
          tasks:[
            {
             created: '230 Sep 2017 22:03:47',
              from:'Fandlyho',
              to:'Hlavna stanica',
              comment:'Bude to lacnejsie ako si mysli',
              timetoFix:'25',
              offeredPrice:'15',
              driver:'Duro',
              status:'Fici',
            }
          ]
        }
      ] 
      }
  });
}
