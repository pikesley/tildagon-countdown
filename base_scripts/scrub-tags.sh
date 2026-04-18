for tag in $(git tag | grep -E "[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}")
do
    echo ${tag}
    git tag --delete ${tag}
done

git tag
