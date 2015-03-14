module.exports = (grunt) ->
    grunt.initConfig(
        pkg: grunt.file.readJSON('package.json')
        concat:
            options:
                separator: ';'
            dist:
                src: ['apps/frontend/src/js/main.js', 'apps/frontend/src/js/**/*.js']
                dest: 'assets/js/script.js'
        jshint:
            files: ['<%= concat.dist.src %>']
        watch:
            files: ['<%= jshint.files %>']
            tasks: ['jshint', 'concat']
    )

    grunt.loadNpmTasks('grunt-contrib-concat')
    grunt.loadNpmTasks('grunt-contrib-watch')
    grunt.loadNpmTasks('grunt-contrib-jshint')
    grunt.registerTask('default', ['concat', 'jshint', 'watch'])
