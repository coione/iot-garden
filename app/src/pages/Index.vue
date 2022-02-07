<template>
  <q-page 
    class="flex"
  >
    <div
      class="full-width"
    >
      <q-card
        style="max-width: 500px; margin: 50px auto;"
      >
        <q-card-section>
          <div class="text-h6">
            Activities
            <q-spinner
              color="secondary"
              size="0.7em"
              v-if="spinner"
            />
            <q-btn 
              @click="confirm = true"
              fab
              class="q-ml-lg float-right"
              color="secondary"
              icon="mdi-watering-can"
            ></q-btn>

            <q-dialog v-model="confirm" persistent>
              <q-card>
                <q-card-section class="row items-center">
                  <q-avatar icon="mdi-water" color="secondary" text-color="white" />
                  <span class="q-ml-sm">Do you want to watering?</span>
                </q-card-section>

                <q-card-actions align="right">
                  <q-btn flat label="Cancel" color="secondary" v-close-popup />
                  <q-btn flat label="Yes" color="secondary" v-close-popup @click="wateringApiCall" />
                </q-card-actions>
              </q-card>
            </q-dialog>
          </div>
        </q-card-section>
        <q-separator />
        <q-card-section>
          <q-list>
            <q-item v-for="(item) in activities" :key="item.id">
              <q-item-section
                side
              >
                <q-icon
                  name="mdi-water"
                  color="secondary"
                />
              </q-item-section>
              <q-item-section
                side
              >
                {{item.type}}
              </q-item-section>
              <q-item-section>
                {{item.value}} cms2
              </q-item-section>
              <q-item-section>
                {{item.date}}
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { ref } from "vue";
import { api } from 'boot/axios';

export default {
  components: {},
  name: "PageIndex",
  setup () {
    return {
      confirm: ref(false),
      spinner: ref(false)
    }
  },
  data () {
    return {
      activities: []
    }
  },
  created () {
    this.loadData()
  },
  methods: {
    loadData () {
      let currentObj = this

      api.get('/activities')
      .then((response) => {
        let data = response.data

        currentObj.activities = []
        data.reverse().forEach(function (item) {
          currentObj.activities.push(item)
        });
      })
      .catch(() => {
        this.$q.notify({
          message: 'failed',
          color: 'negative',
          icon: 'mdi-alert-circle',
          position: 'top'
        })
      })
    },
    wateringApiCall (data) {
      let currentObj = this
      currentObj.spinner = true

      let postData = {
        type: 'watering'
      }

      api.post('/activities', postData)
      .then((response) => {
        let data = response.data

        currentObj.activities = []
        data.reverse().forEach(function (item) {
          currentObj.activities.push(item)
        });

        currentObj.spinner = false
        this.$q.notify({
          message: 'done',
          icon: 'mdi-check',
          color: 'positive',
          position: 'top'
        })
      })
      .catch((err) => {
        currentObj.spinner = false
        let message = 'failed';

        if (err.response.data.message) {
          message = err.response.data.message;
        }

        this.$q.notify({
          message: message,
          color: 'negative',
          icon: 'mdi-alert-circle',
          position: 'top'
        })
      })
    }
  }
}
</script>