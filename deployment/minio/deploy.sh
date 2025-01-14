files=("secret.yaml" "statefulset.yaml" "service.yaml" "network-policy.yaml")

for file in "${files[@]}"; do
    echo $file    
    oc apply -f "$file"
done

