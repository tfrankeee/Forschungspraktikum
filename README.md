# QTI Learning App

## Setup

### 1. Install Node.js >= 16
QTI 3 Item Player Controller was originally built and tested with Node v16.14.  As of November 2023, QTI 3 Item Player Controller has been built and tested with Node v20.9.0.

### 2. Project Setup
run
```sh
npm install
```
and ignore all warnings :D

### 3. Compiles and hot-reloads for development
```sh
npm run serve
```

If you encounter an error about digital envelope routines::unsupported, this error was introduced in Node version >= 17 which changes the crypto hashing function.  There are a number of easy workarounds for this.  For example: 

On Windows systems -
```sh
set NODE_OPTIONS=--openssl-legacy-provider
```

On Linux-like systems (Mac OS, Linux, Git bash, etc.) -
```sh
export NODE_OPTIONS=--openssl-legacy-provider
```

### 4. Open Browser
Open http://localhost:8080/ in the browser.

## Questions
You can see the sample question in public/questions/frage1.xml. 
You can add your own questions (QTI 3.0!) to this directory. Right now the Website has no functionality to cycle between questions, so you have to edit the path to your questions in src/App.vue by yourself (inside ``fetch()`` method):

```js
handlePlayerReady(player) {
      this.qti3Player = player

      const config = {
        guid: "frage001",
        status: "interacting"
      }

      fetch("questions/frage1.xml")
        .then((res) => res.text())
        .then((xml) => {
          this.qti3Player.loadItemFromXml(xml, config)
        })
```
