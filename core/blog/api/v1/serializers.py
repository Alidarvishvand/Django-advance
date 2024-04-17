from rest_framework import serializers
from ...models import Post,Category
from accounts.models import Profile
class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relaitive_url = serializers.URLField(source='get_absolute_api_url', read_only = True)
    absolute_url = serializers.SerializerMethodField(method_name='get_abs_url')
    category = serializers.SlugRelatedField(many=False,slug_field='name',queryset=Category.objects.all())
    
 
    
    class Meta:
        model  = Post
        fields = ['id','author','title', 'content','category','absolute_url','image',
                  'snippet','status', 'created_date', 'published_date','relaitive_url']
        read_only_fields = ['author']
    def get_abs_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
        # build_absolute_uri(obj.pk)
    
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet',None)
            rep.pop('relative_url',None)
            rep.pop('absolute_url',None)
        else :
            rep.pop('content',None)
                  
        rep['category'] = CategorySerializers(instance.category,context={'request':request}).data
        return rep
    
    
    def create(self, validated_data):
       
        validated_data['author'] =Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validated_data)
    

    
    
    
    
    
    

class CategorySerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['name', 'id']
   
 
# class PostSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Post
#             fields = ['id', 'title', 'content','status', 'created_date', 'published_date']
    