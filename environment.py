# runningMode = "deploy_"
runningMode = "dev_"

logLevelStringUpper = "WARNING" if runningMode == "deploy_" else "DEBUG"
logLevelStringLower = "warning" if runningMode == "deploy_" else "debug"

