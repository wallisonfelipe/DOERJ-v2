const shell = require('shelljs')

execute();

setInterval(() => {
    execute();
}, 1000 * 60 * 30) // Executa a cada 30 minutos

function execute()
{
    if (new Date().getHours() >= 18 || new Date().getHours() <= 7) {
        console.log('Horário de descanso, script não será executado ' + new Date().toLocaleString())
        return;
    }

    console.log(`\n\nExecutando script em: ${new Date().toLocaleString()}\n\n`)
    shell.exec('python3 index.py')
}