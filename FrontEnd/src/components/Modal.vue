<template>
  <div class="modal">
    <div class="modal__container">
      <div class="modal__featured">
        <button
          type="button"
          class="button--transparent button--close"
          @click="close"
        >
          <svg
            class="nc-icon glyph"
            x="0px"
            y="0px"
            width="32px"
            height="32px"
            viewBox="0 0 32 32"
          >
            <g>
              <path
                fill="#ffffff"
                d="M1.293,15.293L11,5.586L12.414,7l-8,8H31v2H4.414l8,8L11,26.414l-9.707-9.707 C0.902,16.316,0.902,15.684,1.293,15.293z"
              ></path>
            </g>
          </svg>

          <span class="visuallyhidden">Return to Product Page</span>
        </button>
        <div class="modal__circle"></div>
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/BR_Dachmarke.svg/2000px-BR_Dachmarke.svg.png"
          class="modal__product"
        />
      </div>
      <div class="modal__content overflow-auto">
        <h2><slot name="header"></slot></h2>
        <br />
        <slot name="body" class="overflow-auto"></slot>
      </div>
      <!-- END: .modal__content -->
    </div>
    <!-- END: .modal__container -->
  </div>
</template>

<script>
export default {
  name: "Modal",
  methods: {
    close() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.visuallyhidden {
  border: 0;
  clip: rect(0 0 0 0);
  height: 1px;
  margin: -1px;
  overflow: hidden;
  padding: 0;
  position: absolute;
  width: 1px;
}

body {
  font-family: "Open Sans", sans-serif;
  color: #1a1a1a;
  background-color: #f0f0f0;
}

.button {
  color: #ffffff;
  background-color: #24cf5f;
  padding: 12px 25px;
  font-size: 12px;
  letter-spacing: 1px;
  text-transform: uppercase;
  border: 0;
  border-radius: 2px;
  outline: 0;
  box-shadow: 3px 3px 20px rgba(0, 0, 0, 0.2);
  transition: all 0.2s;
}
.button:hover,
.button:active,
.button:focus {
  -ms-transform: scale(1.1);
  transform: scale(1.1);
}

.button--transparent {
  background: transparent;
  border: 0;
  outline: 0;
}

.button--close {
  position: absolute;
  top: 10px;
  left: 10px;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  -ms-flex-pack: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  color: white;
  border-radius: 50%;
  transition: all 0.25s;
  z-index: 10;
  background-color: #0c8cd3;
}
.button--close svg {
  width: 20px;
  height: 20px;
}
.button--close svg * {
  fill: currentColor;
}
.button--close:hover,
.button--close:active,
.button--close:focus {
  color: black;
  background-color: #ffffff;
  box-shadow: 3px 3px 20px rgba(0, 0, 0, 0.1);
}

.modal {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-pack: center;
  justify-content: center;
  -ms-flex-align: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  padding-top: 200px;
  z-index: 100;
  overflow-y: auto;
  overflow-x: auto;
  background-color: rgba(0, 0, 0, 0.7);
}
.modal__container {
  resize: both;
  display: -ms-flexbox;
  display: flex;
  width: 675px;
  min-height: 400px;
  margin-bottom: 125px;
  background-color: #ffffff;
  border-radius: 5px;
  box-shadow: 3px 3px 20px rgba(0, 0, 0, 0.1);
}
.modal__featured {
  position: relative;
  -ms-flex: 1;
  flex: 1;
  min-width: 230px;
  padding: 20px;
  overflow: hidden;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
}
.modal__circle {
  position: absolute;
  top: -10px;
  left: -5px;
  height: 130%;
  width: 100%;
  background-image: url("https://www.climaplan.de/wp-content/uploads/2020/02/BR-Format.jpg");
  background-size: auto;
  border-radius: 50%;
  /* -ms-transform: translateX(-50%) translateY(-25%); */
  transform: translateX(-60px) translateY(-20px);
}
.modal__product {
  position: relative;
  top: 0;
  left: 55%;
  max-width: 85%;
  -ms-transform: translateX(calc(-50% - 10px));
  transform: translateX(calc(-50% - 10px));
}
.modal__content {
  -ms-flex: 3;
  flex: 3;
  padding: 40px 30px;
  resize: both;
}
</style>