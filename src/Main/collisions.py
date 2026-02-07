__all__ = ['CollisionInfo', 'CollisionHandler']


class CollisionInfo(object):
    """ This class contains all the information about a collision
    """
    def __init__(self, first_collider_object_id, second_collider_object_id):
        self.first_collider_object_id = first_collider_object_id
        self.second_collider_object_id = second_collider_object_id


class CollisionHandler(object):
    def __init__(self, world):
        self._world = world

    def handle(self):
        collision_list = self._build_collision_list()
        if len(collision_list) == 0:
            return

        world_object_list = self._world.get_objects_list()
        for collision_item in collision_list:
            # retrieve the object. Remember that the key of the dictionary
            # is the object ID of the object that detected a collision
            object = world_object_list[collision_item]
            collision_info = collision_list[collision_item]
            object.collision_handler(collision_info, self._world)

    def _build_collision_list(self):
        # We prepare a dictionary where the key is the ID of the object that has a collision
        # and the value is a CollisionInfo that contains the information about
        # the other object that collided
        # N.B. We can have a better collision detection algorithm. With this one, we are not
        # able to detect multiple collision for the same object (for example, an object that
        # collide with two other different objects
        collisions = {}

        for first_object_id in self._world.get_objects_list():
            if first_object_id in collisions:
                continue
            for second_object_id in self._world.get_objects_list():
                if second_object_id in collisions:
                    continue

                if first_object_id == second_object_id:
                    continue

                # Retrieve the collision circles and check if there is a collision
                world_objects_list = self._world.get_objects_list()
                first_circle = world_objects_list[first_object_id].collision_circle
                second_circle = world_objects_list[second_object_id].collision_circle
                is_collision = first_circle.is_intersecting_circle(second_circle)

                if is_collision:
                    collisions[first_object_id] = CollisionInfo(first_object_id, second_object_id)
                    collisions[second_object_id] = CollisionInfo(second_object_id, first_object_id)

        return collisions