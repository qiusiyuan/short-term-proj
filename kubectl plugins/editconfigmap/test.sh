#!/bin/bash
calling_directory=$1
configmap_name=$2
temp_json_file_name=".${configmap_name}_temp.json"

function delete_call {
  read -p "Delete the temp configmap json file: ${calling_directory}/${temp_json_file_name}?(y/n) : " delete_answer
  if [[ ${delete_answer} = "y" ]]; then
    rm -f ${calling_directory}/${temp_json_file_name}
    echo "Deleted"
  fi
}

if [[ -z ${configmap_name} ]]; then
  echo "editconfigmap requires 1 argument {configmapName}" && exit 1
fi
## check existence of the configmap
kubectl get configmap --namespace ${KUBECTL_PLUGINS_CURRENT_NAMESPACE} ${configmap_name}
retCode=$?
if [[ ${retCode} -eq 1 ]]; then
  exit 1
fi
## save the config map as a temp json file
kubectl get configmap --namespace ${KUBECTL_PLUGINS_CURRENT_NAMESPACE} ${configmap_name} -o json > ${calling_directory}/${temp_json_file_name}

## run python script to add field in json
python edit_configmap_json.py ${temp_json_file_name} ${calling_directory}
retCode=$?
if [[ ${retCode} -eq 1 ]]; then
  delete_call
  exit 1
fi

## show the edited file
cat ${calling_directory}/${temp_json_file_name}
echo
read -p "Verify above configmap json is what you want to deploy (y/n): " verify_answer
if [[ ${verify_answer} = "y" ]]; then
  kubectl replace -f ${calling_directory}/${temp_json_file_name}
fi

delete_call