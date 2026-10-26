# RPM build of [chromebook-linux-audio](https://github.com/WeirdTreeThing/chromebook-linux-audio)
[![Copr build status](https://copr.fedorainfracloud.org/coprs/pvermeer/chromebook-linux-audio/package/chromebook-linux-audio/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/pvermeer/chromebook-linux-audio/package/chromebook-linux-audio/)

Allows the [chromebook-linux-audio](https://github.com/WeirdTreeThing/chromebook-linux-audio) script to run on immutable Fedora installations.

It's not perfect. If audio still doesnt work you can look at the output with:
```sh
journalctl -t 'rpm-ostree(chromebook-linux-audio.post)'
```

### Fedora copr
https://copr.fedorainfracloud.org/coprs/pvermeer/chromebook-linux-audio

### Credits
- https://github.com/WeirdTreeThing
- https://github.com/mikaelvz/chromebook-linux-audio

If you would like to support the work [WeirdTreeThing](https://github.com/WeirdTreeThing) does, checkout his GitHub [here](https://github.com/WeirdTreeThing).
